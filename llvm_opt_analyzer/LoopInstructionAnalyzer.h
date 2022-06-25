#ifndef LLVM_TRANSFORMS_LOOPINSTRUCTIONANALYZER_H
#define LLVM_TRANSFORMS_LOOPINSTRUCTIONANALYZER_H

#include "llvm/IR/PassManager.h"
#include "llvm/Analysis/LoopAnalysisManager.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"

namespace llvm {
  

class Loop;
class LPMUpdater;

class LoopInstructionAnalyzerPass : public PassInfoMixin<LoopInstructionAnalyzerPass> {
public:
  PreservedAnalyses run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U);
};

} // namespace llvm

#endif // LLVM_TRANSFORMS_LOOPINSTRUCTIONANALYZERD_H