#ifndef LLVM_TRANSFORMS_LOOPANALYZER_H
#define LLVM_TRANSFORMS_LOOPANALYZER_H

#include "llvm/IR/PassManager.h"
#include "llvm/Analysis/LoopAnalysisManager.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"

namespace llvm {
  

class Loop;
class LPMUpdater;

class LoopAnalyzerPass : public PassInfoMixin<LoopAnalyzerPass> {
public:
  PreservedAnalyses run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U);
};

} // namespace llvm

#endif // LLVM_TRANSFORMS_LOOPANALYZER_H