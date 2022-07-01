import sys
import json
import numpy as np

###################################################
# An API for gathering statistics for various loops
###################################################

class LoopStat:

    AllLoopAttributes = []    
    def __init__(self,InputString: str) -> None:
        self.LoopAttributes = {}

        attributes = InputString.split("|")
        for attr in attributes:
            attr_list = attr.split(",")
            self.LoopAttributes[attr_list[0]] = attr_list[1:] if len(attr_list) > 1 else []
        
        self.LoopAttributes["Filename"] = self.LoopAttributes["Filename"][0]
        self.LoopAttributes["LoopLine"] = int(self.LoopAttributes["LoopLine"][0])
        self.LoopAttributes["LoopLimInferred"] = int(self.LoopAttributes["LoopLim"][1])-1
        self.LoopAttributes["LoopLim"] = int(self.LoopAttributes["LoopLim"][0])
        self.LoopAttributes["VectorizationHint"] = True if self.LoopAttributes["VectorizationHint"][0] == "1" else False

        subloops = []
        for i in range(0,len(self.LoopAttributes["Subloops"]),2):
            subloops.append((self.LoopAttributes["Subloops"][i],int(self.LoopAttributes["Subloops"][i+1])))

        self.LoopAttributes["Instructions"] = [int(x) for x in self.LoopAttributes["Instructions"]]
        self.LoopAttributes["Outermost"] = True if self.LoopAttributes["NestingLevel"][1] == '1' else False
        self.LoopAttributes["Innermost"] = True if self.LoopAttributes["NestingLevel"][2] == '1' else False
        self.LoopAttributes["NestingLevel"] = int(self.LoopAttributes["NestingLevel"][0])
        self.LoopAttributes["Subloops"] = list(subloops)
        LoopStat.AllLoopAttributes.append(self.LoopAttributes)

    def searchForSubloop(filename,loopline):
        for item in LoopStat.AllLoopAttributes:
            if item["Filename"] == filename and item["LoopLine"] == loopline:
                return item
        return None

    def getTotalOpsGlobal(filename,loopline):
        CL = LoopStat.searchForSubloop(filename,loopline)
        if CL["LoopLim"] > 0:
            operations = CL["LoopLim"] * np.array(CL["Instructions"],dtype=int)
        elif CL["LoopLimInferred"] > 0:
            operations = CL["LoopLimInferred"] * np.array(CL["Instructions"],dtype=int)
        else:
            return np.zeros(len(CL["Instructions"]),dtype=int)
        for subl in CL["Subloops"]:
            operations += np.array(LoopStat.getTotalOpsGlobal(*subl))
        return operations

    def getLoopLine(self): return self.LoopAttributes["LoopLine"]
    def getLoopFilename(self): return self.LoopAttributes["Filename"]
    def getSubloops(self): return self.LoopAttributes["Subloops"]
    def getNestingLevel(self): return self.LoopAttributes["NestingLevel"]
    def isInnermost(self): return self.LoopAttributes["Innermost"]
    def isOutermost(self): return self.LoopAttributes["Outermost"]
    def getLoopLimit(self): return self.LoopAttributes["LoopLim"]
    def getLoopLimitBestEffort(self):
        ll = self.getLoopLimit()
        if ll > 0:
            return ll
        return self.LoopAttributes["LoopLimInferred"]
    def getInstructionsRecursive(self): return LoopStat.getTotalOpsGlobal(self.getLoopFilename(),self.getLoopLine()).tolist()
    def getInstructionsSuperficial(self): return self.LoopAttributes["Instructions"]
    def getVectorizationHint(self): return self.LoopAttributes["VectorizationHint"]

        
        
'''  
X = LoopStat("Filename,bubble_sort.cpp|LoopLine,18|LoopLim,0,16|Instructions,0,0,5,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,12,0,0,0,0,0,0,0,0,0,0|VectorizationHint,0|NestingLevel,2,0,1|Subloops")
C = LoopStat("Filename,bubble_sort.cpp|LoopLine,17|LoopLim,16,16|Instructions,0,0,10,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,17,0,0,0,0,0,0,0,0,0,0|VectorizationHint,0|NestingLevel,1,1,0|Subloops,bubble_sort.cpp,18")

print(LoopStat.AllLoopAttributes)
print("\n")

print(f"{X.getInstructionsRecursive()}, {X.getInstructionsSuperficial()}, {X.getLoopFilename()}, {X.getNestingLevel()}, {X.getLoopLimitBestEffort()}, {X.getLoopLimit()}, {X.getVectorizationHint()}, {X.getSubloops()}, {X.isInnermost()}, {X.isOutermost()}, {X.getLoopLine()}")
'''