#include "llvm/Transforms/Utils/LoopInstructionAnalyzer.h"
#include "llvm/Analysis/LoopAnalysisManager.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/IR/DebugInfoMetadata.h"
#include "llvm/IR/DebugInfo.h"
#include <iostream>
#include <fstream>
using namespace llvm;

/*
* WARNING: This File must be placed in the correct LLVM directory
* and recompiled with the entire project. The Component must also
* be registered AS A LOOP PASS in the appropriate lists.
*/


// WARNING: to be used as a STANDALONE pass. Disable all optimizations
// with -O0 at compile time, enable -g debug mode and -Xclang -disable-O0-optnone
// to allow Transform Passes.
// ------------- Loop Instruction Counter Prototype -----------------


PreservedAnalyses LoopInstructionAnalyzerPass::run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U)
{
    unsigned mem_read = 0,mem_write = 0,arithmetic =0,lloc=-1;
    bool first_instr = true;
    const ArrayRef< BasicBlock * > BBAR = L.getBlocks();
    for (size_t i=0;i<BBAR.size();i++)
    {
        for (const Instruction &INSTR: *BBAR[i])
        {
            if (first_instr)
            {
                first_instr = false;
                if (DILocation *Loc = INSTR.getDebugLoc())
                    lloc = Loc->getLine();
            }
            switch (INSTR.getOpcode())
            {
                case Instruction::Add:// add
                    arithmetic++;
                    break;
                case Instruction::Sub:// add
                    arithmetic++;
                    break;
                case Instruction::Load:
                    mem_read++;
                    break;
                case Instruction::Store:
                    mem_write++;
                    break;
                default:
                    break;
            }
        }
    }
    outs() << "Loop: " << lloc << " Instructions -> " <<" arr: "<<arithmetic<<", load: "<<mem_read<<", store: "<<mem_write<<"\n";   
    return PreservedAnalyses::all();
}