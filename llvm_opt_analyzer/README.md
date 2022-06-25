# Static Analysis with LLVM (clang + opt)

## Setup

To setup this project LLVM must be built from source. This section of the project started in June 2022 and is meant to be used with the current LLVM Release **LLVM 14.0.5**

### Download and build for the first time
```bash
git clone --depth=1 https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir build
cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -DLLVM_ENABLE_ASSERTIONS=On -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../llvm
make
```

---
Notes:
1. ```git clone --depth=1 https://github.com/llvm/llvm-project.git``` downloads ONLY THE LATEST version. In the future you might need to clone the entire project and checkout to an old commit to reach the current version (LLVM 14.0.5).
1. ```-DLLVM_ENABLE_ASSERTIONS=On ``` Is NECESSARY for opt in order to gather information.

---

### Adding our custom pass to opt

In this folder you will find two files:
1. LoopInstructionAnalyzer.h
1. LoopInstructionAnalyzer.cpp

These files must be copied to:

1. ```llvm-project/llvm/include/llvm/Transforms/Utils/LoopInstructionAnalyzer.h```
1. ```llvm-project/llvm/lib/Transforms/Utils/LoopInstructionAnalyzer.cpp```

Once this is done you will need to make the .cpp files visible to CMAKE. To do this simply add its name to

 ```llvm-project/llvm/lib/Transforms/Utils/CMakeLists.txt```

Finally, the new pass must be registered with the rest of the preexesting passes. To do this add the line:

```LOOP_PASS("loop-instr", LoopInstructionAnalyzerPass())```

to the LOOP_PASS section of the file:

 ```llvm-project/llvm/lib/Passes/PassRegistry.def```

Also, add:

```#include llvm/include/llvm/Transforms/Utils/LoopInstructionAnalyzer.h```

to the file:

 ```llvm-project/llvm/lib/Passes/PassBuilder.cpp```

 **Once all of the above have been done, recompile with:**
 ```bash
 cmake -DLLVM_ENABLE_PROJECTS=clang -DLLVM_ENABLE_ASSERTIONS=On -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../llvm
make
 ```

 **DONE**

 ## Usage

 To use the tool, we have created a Makefile in this directory. Simply use:

 ```bash
 make <path/to/source/file>.stat
 ```
 for any source file ending in .cpp


