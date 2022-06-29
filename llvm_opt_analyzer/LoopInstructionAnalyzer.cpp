#include "llvm/Transforms/Utils/LoopInstructionAnalyzer.h"
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

PreservedAnalyses LoopInstructionAnalyzerPass::run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U)
{   
    char loopFilename[FILENAME_LIM];
    const ArrayRef< BasicBlock * > BBAR = L.getBlocks();
    unsigned InstructionCountArr[InstrAnalysisCount],lloc=0;

    LoopAccessInfo LAI = LoopAccessInfo(&L,&(AR.SE),&(AR.TLI),&(AR.AA),&(AR.DT),&(AR.LI));
    //PredicatedScalarEvolution PSE = PredicatedScalarEvolution(AR.SE,L);
    //MemoryDepChecker MDC = MemoryDepChecker(PSE,&L);

    for (int i=0;i<InstrAnalysisCount;i++)
        InstructionCountArr[i]=0;

    lloc = L.getStartLoc()->getLine();
    strcpy(loopFilename,(L.getStartLoc()->getFilename()).data());
    for (size_t i=0;i<BBAR.size();i++)
        for (Instruction &INSTR: *BBAR[i])
        {
            InstructionCountArr[INSTR.getOpcode()]++;
            //if (L.isInnermost() and (isa <LoadInst> (INSTR) or isa <StoreInst> (INSTR)))
                //MDC.addAccess(&INSTR);
        }
 
    outs() << "Filename,"<<loopFilename<<"|"<<"LoopLine," << lloc << "|LoopLim," <<  AR.SE.getSmallConstantTripCount(&L) <<"|Instructions"; 
    for (int i=0;i<InstrAnalysisCount;i++)
        outs()<<","<<InstructionCountArr[i];
    outs() << "|VectorizationHint," << LAI.canVectorizeMemory() << "\n";
    return PreservedAnalyses::all();
}