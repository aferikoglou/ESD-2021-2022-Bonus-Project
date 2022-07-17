import sys
import json
import subprocess
import os

HLS_INPUT_FILE = sys.argv[1]
KERNEL_INFO_PRECURSOR = "hls_extracted_locs.txt"
DIRNAME,PLAIN_NAME = os.path.split(HLS_INPUT_FILE)
print(PLAIN_NAME)
if DIRNAME == "": DIRNAME = "."
POLLY_OPT_FILE =PLAIN_NAME.split(".")[0] + ".p_stat"

######## Create polly information file ##########

print("=================== LLVM Polly Analysis =====================")

with open("polly_output.txt",'w') as pout:
    polly = subprocess.Popen(["make","-f","makefiles/Makefile",f"{DIRNAME}/{POLLY_OPT_FILE}"],stdout=pout)
    polly.wait()

pollyLines = []
with open("polly_output.txt",'r') as pout:
    pollyLines = pout.readlines()

analysisLines = []
for line in pollyLines:
    if "^pollyAnalysis@@" in line:
        analysisInfo = line.split("@@|")[1][:-1].split("|")
        LLine = int(analysisInfo[0].split(":")[1])
        LFile = analysisInfo[1].split(":")[1]
        LParallel =  bool(int(analysisInfo[2].split(":")[1]))
        analysisLines.append({"LoopFile": LFile,"LoopLine":LLine,"Parallel": LParallel})
            


ResultDict = {}
for line in analysisLines:
    ResultDict[line["LoopFile"] + "/"+ str(line["LoopLine"])] = False

for line in analysisLines:
    ResultDict[line["LoopFile"] + "/"+ str(line["LoopLine"])] = ResultDict[line["LoopFile"] + "/"+ str(line["LoopLine"])] or line["Parallel"]



kipLines = []
with open(KERNEL_INFO_PRECURSOR,'r') as kip:
    kipLines=kip.readlines()

parallelDictResults = {}
for line in kipLines:
    tmp = line.split(",")
    if tmp[0] == 'L':
        parallelDictResults[f"L{tmp[3][:-1]}"] = ResultDict[f"{PLAIN_NAME}/{int(tmp[1])+1}"]

print(parallelDictResults)

with open(f"{DIRNAME}/polly_analysis.json",'w') as paj:
    json.dump(parallelDictResults,paj)

