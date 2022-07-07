import sys
import json
import numpy as np
import os
import subprocess


class SourceStatistics:
    def __init__(self,source_file:str) -> None:
        self.loops = {}
        self.src = source_file
    
    def addLoop(self,loop_string:str):
        attribute_list = loop_string.split()[0].split("|") # split at "|" after removing last whitespace
        temp_dict = dict()
        for attr in attribute_list:
            split_list = attr.split(",") #split at ","
            temp_dict[split_list[0]] = split_list[1:] if len(split_list) > 1 else [] # (if list is not empty) 
        
        temp_dict["Filename"] = temp_dict["Filename"][0]
        temp_dict["LoopLine"] = int(temp_dict["LoopLine"][0]) - 1
        id = temp_dict["ID"][0]
        temp_dict.pop("ID",None)
        temp_dict["InlinedInstance"] = True if temp_dict["InlinedInstance"][0] == '1' else False
        
        loop_lims = temp_dict["LoopLim"]
        temp_dict["LoopLimActual"] = int(loop_lims[0]) - 1
        temp_dict["LoopLimInferred"] = int(loop_lims[1]) - 1
        temp_dict.pop("LoopLim",None)

        temp_dict["Instructions"] = list([int(x) for x in temp_dict["Instructions"]])
        temp_dict["VectorizationHint"] = True if temp_dict["VectorizationHint"][0] == "1" else False

        level,outermost,innermost = tuple([int(x)for x in temp_dict["NestingLevel"]])
        temp_dict["NestingLevel"] = level
        temp_dict["Outermost"] = bool(outermost)
        temp_dict["Innermost"] = bool(innermost)

        print(temp_dict)
        self.loops[id] = dict(temp_dict)

    def _generateLocalOps(self):
        for loop in self.loops:
            self.loops[loop]["LocalOps"] = np.array(self.loops[loop]["Instructions"],dtype=int)
            for subloop in self.loops[loop]["Subloops"]:
                self.loops[loop]["LocalOps"] -= np.array(self.loops[subloop]["Instructions"],dtype=int)
            self.loops[loop]["LocalOps"] = self.loops[loop]["LocalOps"].tolist()

    def _generateTotalOps_aux(self,loop: str):
        if "TotalOps" in self.loops[loop]: # if value is precomputed
            return self.loops[loop]["TotalOps"]
        actualLim = self.loops[loop]["LoopLimActual"]
        inferredLim = self.loops[loop]["LoopLimInferred"]

        lLim = 0
        if actualLim > 0:
            lLim = actualLim
        elif inferredLim > 0:
            lLim = inferredLim

        totalOps = lLim * np.array(self.loops[loop]["LocalOps"])
        for subl in self.loops[loop]["Subloops"]:
            totalOps += lLim * np.array(self._generateTotalOps_aux(subl),dtype=int)
        self.loops[loop]["TotalOps"] = totalOps.tolist()
        return self.loops[loop]["TotalOps"]

    def generateTotalOps(self):
        for loop in self.loops:
            self._generateTotalOps_aux(loop)


    def setCodeFunctions(self,functions):
        self.functions = {}
        for f in functions:
            self.functions[f[0]] = dict({"start": int(f[1]),"end":int(f[2])}) # start and end of function

    def setTLF(self,topLevelFunction: str):
        self.TLF = topLevelFunction
    

    def estimateFunctionOps(self):
        for f in self.functions:
            subls = []
            start,end = (self.functions[f]["start"],self.functions[f]["end"])
            for loop in self.loops:
                if (self.src in self.loops[loop]["Filename"]) and start <= self.loops[loop]["LoopLine"] and end >= self.loops[loop]["LoopLine"] and self.loops[loop]["Outermost"]:
                    if self.TLF == f:
                        subls.append(loop)
                    elif not self.loops[loop]["InlinedInstance"]:
                        subls.append(loop)
            self.functions[f]["ActiveLoops"] = list(subls)
            self.functions[f]["FunctionOps"] = np.zeros(67)
            for subl in subls:
                self.functions[f]["FunctionOps"] += np.array(self.loops[subl]["TotalOps"],dtype=int)
            self.functions[f]["FunctionOps"] = self.functions[f]["FunctionOps"].tolist()


    def linkLinesToTags(self,kernel_info_precursor:str):
        self.LinesToTags = {}
        with open(kernel_info_precursor,'r') as kip:
            kip_lines = kip.readlines()
        for line in kip_lines:
            if line[0] == "L":
                tmp = line.split(",")
                self.LinesToTags[str(tmp[1])] = f"L{tmp[3]}"


    def generateSourceInfo(self,outfile:str):
        outDict = {}
        totalCodeOps = np.zeros(67)
        for function in self.functions:
            totalCodeOps += np.array(self.functions[function]["FunctionOps"],dtype=int)
        totalCodeOps = totalCodeOps.tolist()

        TLFOps = self.functions[self.TLF]["FunctionOps"]

        NonInlinedLoops = {}
        for loop in self.loops:
            if not self.loops[loop]["InlinedInstance"]:
                NonInlinedLoops[self.LinesToTags[str(self.loops[loop]["LoopLine"])]] = dict(self.loops[loop])

        outDict = {"TotalCodeOps": totalCodeOps, "TLFOps": TLFOps,"functions":self.functions, "loops": NonInlinedLoops}
        with open(outfile,"w") as src_info:
            json.dump(outDict,src_info)


HLS_INPUT_FILE = sys.argv[1]
TLF = sys.argv[2]
KERNEL_INFO_PRECURSOR = "hls_extracted_locs.txt"
SRC_INFO_PRECURSOR = "opt_inline_analysis.txt"
FN_DECLS = "hls_function_declarations.txt"
DIRNAME,PLAIN_NAME = os.path.split(HLS_INPUT_FILE)
print(PLAIN_NAME)
if DIRNAME == "": DIRNAME = "."
SRC_OPT_FILE =PLAIN_NAME.split(".")[0] + ".s_stat"

print("\n============ Source Info Generator ============")
with open(SRC_INFO_PRECURSOR,'w') as opt_analysis:
    p = subprocess.Popen(["make","-f","makefiles/Makefile",f"{DIRNAME}/{SRC_OPT_FILE}"],stdout=opt_analysis)
    p.wait()


SourceAnalysis = SourceStatistics(PLAIN_NAME)
with open(SRC_INFO_PRECURSOR,'r') as opt_analysis:
    lines = opt_analysis.readlines()

for line in lines:
    if "NestingLevel" in line:
        SourceAnalysis.addLoop(line)

SourceAnalysis._generateLocalOps()
SourceAnalysis.generateTotalOps()

with open(FN_DECLS,"r") as fnd:
    function_decls = fnd.readlines()

fn_tuples = []
for line in function_decls:
    fn_tuples.append(tuple(line.split(",")))

SourceAnalysis.setCodeFunctions(fn_tuples)
SourceAnalysis.setTLF(TLF)
SourceAnalysis.estimateFunctionOps()
SourceAnalysis.linkLinesToTags(KERNEL_INFO_PRECURSOR)
SourceAnalysis.generateSourceInfo("src_info.json")


'''

X = SourceStatistics("bubble_sort.cpp")
with open("stat.txt", "r") as source_info:
    L = source_info.readlines()

for line in L:
    X.addLoop(line)

X._generateLocalOps()
X.generateTotalOps()

X.setCodeFunctions([("r0",3,6),("addArr",8,12),("mai",14,39)])
X.setTLF("mai")
X.estimateFunctionOps()

X.generateSourceInfo("src_info.json")


for item in X.loops:
    print(item,X.loops[item]["Instructions"][:6],X.loops[item]["LocalOps"][:6],X.loops[item]["LoopLimActual"],X.loops[item]["LoopLimInferred"],X.loops[item]["Subloops"],X.loops[item]["TotalOps"])
'''