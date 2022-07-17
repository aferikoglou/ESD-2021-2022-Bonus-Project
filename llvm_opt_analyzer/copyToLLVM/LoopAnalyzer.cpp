#include "llvm/Transforms/Utils/LoopAnalyzer.h"
#include "llvm/Analysis/LoopAnalysisManager.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/IR/DebugInfo.h"
#include "llvm/Analysis/ScalarEvolution.h"
#include "llvm/Analysis/LoopAccessAnalysis.h"
#include "llvm/Transforms/Vectorize/LoopVectorizationLegality.h"
#include "llvm/Pass.h"
#include <iostream>
#include <fstream>
#include <string>
using namespace llvm;

#ifndef FILENAME_LIM
#define FILENAME_LIM 512
#endif 

PreservedAnalyses LoopAnalyzerPass::run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U)
{   
    char loopFilename[FILENAME_LIM];
    unsigned lloc=0;
    LoopAccessInfo LAI = LoopAccessInfo(&L,&(AR.SE),&(AR.TLI),&(AR.AA),&(AR.DT),&(AR.LI));
    lloc = L.getStartLoc()->getLine();
    strcpy(loopFilename,(L.getStartLoc()->getFilename()).data());
    outs() << "Filename," << loopFilename;
    outs() << "|LoopLine," << lloc;
    outs() << "|ID," << &L;
    outs() << "|LoopLimActual," << AR.SE.getSmallConstantTripCount(&L);
    outs() << "|LoopLimInferred," << AR.SE.getSmallConstantMaxTripCount(&L);
    outs() << "|VectorizationHint," << LAI.canVectorizeMemory();
    outs() << "|NestingLevel," << L.getLoopDepth();
    outs() << "|Outermost," << L.isOutermost();
    outs() << "|Innermost," << L.isInnermost();
    outs() << "|Subloops";
    for (auto & LoopIterator : L.getSubLoops())
    {   
        if (L.getLoopDepth() + 1 == LoopIterator->getLoopDepth())
            outs() << "," << LoopIterator;
    }
    outs() << "\n";
    return PreservedAnalyses::all();
}