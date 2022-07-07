import sys
import json

###################################################
# An API for gathering statistics for various loops
###################################################

class LoopStat:

    AllLoopAttributes = []    
    def __init__(self) -> None:
        self.LoopAttributes = {}

    def loadFromString(self,InputString: str):
        attributes = InputString.split("|")
        for attr in attributes:
            attr_list = attr.split(",")
            self.LoopAttributes[attr_list[0]] = attr_list[1:] if len(attr_list) > 1 else []
        
        self.LoopAttributes["Filename"] = self.LoopAttributes["Filename"][0]
        self.LoopAttributes["LoopLine"] = int(self.LoopAttributes["LoopLine"][0])-1
        self.LoopAttributes["LoopLimActual"] = int(self.LoopAttributes["LoopLimActual"][0]) - 1
        self.LoopAttributes["LoopLimInferred"] = int(self.LoopAttributes["LoopLimInferred"][0]) -1
        self.LoopAttributes["LoopLim"] = self.LoopAttributes["LoopLimActual"] if self.LoopAttributes["LoopLimActual"] >= 0 else self.LoopAttributes["LoopLimInferred"]
        self.LoopAttributes["VectorizationHint"] = True if self.LoopAttributes["VectorizationHint"][0] == "1" else False

        self.LoopAttributes["Outermost"] = True if self.LoopAttributes["Outermost"][0] == '1' else False
        self.LoopAttributes["Innermost"] = True if self.LoopAttributes["Innermost"][0] == '1' else False
        self.LoopAttributes["NestingLevel"] = int(self.LoopAttributes["NestingLevel"][0])
        LoopStat.AllLoopAttributes.append(self.LoopAttributes)

    
    def loadFromDict(self,loadDict):
        for key in loadDict:
            self.LoopAttributes[key] = loadDict[key]

    def getLoopLine(self): return self.LoopAttributes["LoopLine"]
    def getLoopFilename(self): return self.LoopAttributes["Filename"]
    def getSubloops(self): return self.LoopAttributes["Subloops"]
    def getNestingLevel(self): return self.LoopAttributes["NestingLevel"]
    def isInnermost(self): return self.LoopAttributes["Innermost"]
    def isOutermost(self): return self.LoopAttributes["Outermost"]
    def getLoopLimit(self): return self.LoopAttributes["LoopLimActual"]
    def getLoopLimitBestEffort(self):
        ll = self.getLoopLimit()
        if ll > 0:
            return ll
        return self.LoopAttributes["LoopLimInferred"]


    def exportLoopData(self):
        exportLog = dict()
        exportLog["LoopLine"] = self.getLoopLine()
        exportLog["Filename"] = self.getLoopFilename()
        exportLog["Subloops"] = self.getSubloops()
        exportLog["NestingLevel"] = self.getNestingLevel()
        exportLog["Innermost"] = self.isInnermost()
        exportLog["Outermost"] = self.isOutermost()
        exportLog["LoopLimActual"] = self.getLoopLimit()
        exportLog["LoopLimInferred"] = self.getLoopLimitBestEffort()
        exportLog["VectorizationHint"] = self.getVectorizationHint()
    
        
'''  
X = LoopStat("Filename,bubble_sort.cpp|LoopLine,18|LoopLim,0,16|Instructions,0,0,5,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,1,12,0,0,0,0,0,0,0,0,0,0|VectorizationHint,0|NestingLevel,2,0,1|Subloops")
C = LoopStat("Filename,bubble_sort.cpp|LoopLine,17|LoopLim,16,16|Instructions,0,0,10,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,3,17,0,0,0,0,0,0,0,0,0,0|VectorizationHint,0|NestingLevel,1,1,0|Subloops,bubble_sort.cpp,18")

print(LoopStat.AllLoopAttributes)
print("\n")

print(f"{X.getInstructionsRecursive()}, {X.getInstructionsSuperficial()}, {X.getLoopFilename()}, {X.getNestingLevel()}, {X.getLoopLimitBestEffort()}, {X.getLoopLimit()}, {X.getVectorizationHint()}, {X.getSubloops()}, {X.isInnermost()}, {X.isOutermost()}, {X.getLoopLine()}")
'''