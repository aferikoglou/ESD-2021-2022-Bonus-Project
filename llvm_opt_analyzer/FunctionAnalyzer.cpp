#include "llvm/Transforms/Utils/FunctionAnalyzer.h"
using namespace llvm;


/// This file follows the helloworld guide instuctions
/// WARNING: It must be put in a similar location
/// WARNING: The function Pass MUST be registered correctly

PreservedAnalyses FunctionAnalyzerPass::run(Function &F,
                                      FunctionAnalysisManager &AM) {

  errs() << "FunctionDecl: " << F.getName() << " Instcount: " << F.getInstructionCount() <<"\n";
  return PreservedAnalyses::all();
}