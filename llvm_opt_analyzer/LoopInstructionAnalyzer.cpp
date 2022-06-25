#include "llvm/Transforms/Utils/LoopInstructionAnalyzer.h"
#include "llvm/Analysis/LoopAnalysisManager.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/IR/DebugInfo.h"
#include <iostream>
#include <fstream>
using namespace llvm;

#ifndef InstrAnalysisCount 
#define InstrAnalysisCount 67
// Instruction 0 unused
#endif
PreservedAnalyses LoopInstructionAnalyzerPass::run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U)
{
    bool firstInstr = true; // variable that is only true for the first instruction in a loop.
    const ArrayRef< BasicBlock * > BBAR = L.getBlocks(); // Get all basic blocks in a loop
    unsigned InstructionCountArr[InstrAnalysisCount],lloc=-1;

    // Set array of instruction counters to zero
    for (int i=0;i<InstrAnalysisCount;i++)
        InstructionCountArr[i]=0;

    for (size_t i=0;i<BBAR.size();i++) // for every basic block in the loop
    {
        for (const Instruction &INSTR: *BBAR[i]) // for every instruction in the basic block
        {
            if (firstInstr) // execute only for the first instruction in the loop
            {
                firstInstr = false; // if statement will be false from now on
                
                // WARNING: For the following line to work, code must be compiled with "-g" (debug) flag
                if (DILocation *Loc = INSTR.getDebugLoc()) // get line location from debug info
                    lloc = Loc->getLine(); 
            }
            InstructionCountArr[INSTR.getOpcode()]++; // increment counter for the current instruction opcode
        }
    }
    outs() << "LoopLine:" << lloc << ""; 
    for (int i=0;i<InstrAnalysisCount;i++)
        outs()<<","<<InstructionCountArr[i];
    outs()<<"\n";
    return PreservedAnalyses::all();
}