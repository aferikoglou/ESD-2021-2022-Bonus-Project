#include "llvm/Transforms/Utils/InlinedExplorer.h"
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

#ifndef InstrAnalysisCount 
#define InstrAnalysisCount 67
// Instruction 0 unused
#endif

#ifndef FILENAME_LIM
#define FILENAME_LIM 512
#endif 

PreservedAnalyses InlinedExplorerPass::run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U)
{   
    char loopFilename[FILENAME_LIM],subloopFilename[FILENAME_LIM];
    const ArrayRef< BasicBlock * > BBAR = L.getBlocks();
    unsigned InstructionCountArr[InstrAnalysisCount],lloc=0;
    auto containedSubloops = L.getSubLoops();
    bool InlinedInstance = false;
    if (L.getStartLoc().getInlinedAt() != nullptr)
        InlinedInstance = true;
    LoopAccessInfo LAI = LoopAccessInfo(&L,&(AR.SE),&(AR.TLI),&(AR.AA),&(AR.DT),&(AR.LI));

    for (int i=0;i<InstrAnalysisCount;i++)
        InstructionCountArr[i]=0;

    lloc = L.getStartLoc()->getLine();
    strcpy(loopFilename,(L.getStartLoc()->getFilename()).data());
    for (size_t i=0;i<BBAR.size();i++)
        for (Instruction &INSTR: *BBAR[i])
            InstructionCountArr[INSTR.getOpcode()]++;

    outs() << "Filename," << loopFilename;
    outs() << "|LoopLine," << lloc;
    outs() << "|ID," << &L;
    outs() << "|InlinedInstance," << InlinedInstance;
    outs() << "|LoopLim," << AR.SE.getSmallConstantTripCount(&L) << "," << AR.SE.getSmallConstantMaxTripCount(&L); // Actual, Inferred
    outs() <<"|Instructions"; 
    for (int i=0;i<InstrAnalysisCount;i++)
        outs()<<","<<InstructionCountArr[i];
    outs() << "|VectorizationHint," << LAI.canVectorizeMemory();
    outs() << "|NestingLevel," << L.getLoopDepth() << "," << L.isOutermost() << "," <<L.isInnermost();
    outs() << "|Subloops";
    for (auto & LoopIterator : containedSubloops)
    {   
        if (L.getLoopDepth() + 1 == LoopIterator->getLoopDepth())
            outs() << "," << LoopIterator;
    }
    outs() << "\n";
    return PreservedAnalyses::all();
}