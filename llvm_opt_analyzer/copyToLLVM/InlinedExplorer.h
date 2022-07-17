#ifndef LLVM_TRANSFORMS_INLINEDEXPLORER_H
#define LLVM_TRANSFORMS_INLINEDEXPLORER_H

#include "llvm/IR/PassManager.h"
#include "llvm/Analysis/LoopAnalysisManager.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/Analysis/ScalarEvolution.h"

namespace llvm {

class Loop;
class LPMUpdater;

class InlinedExplorerPass : public PassInfoMixin<InlinedExplorerPass> {
public:
  PreservedAnalyses run(Loop &L, LoopAnalysisManager &AM,
                        LoopStandardAnalysisResults &AR, LPMUpdater &U);
};

} // namespace llvm

#endif // LLVM_TRANSFORMS_INLINEDEXPLORER_H