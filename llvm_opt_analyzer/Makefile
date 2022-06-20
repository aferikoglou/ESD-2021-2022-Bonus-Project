CXX = /Users/andkakolyr/Desktop/LLVM/llvm-project/build/bin/clang++
CXXFLAGS = -Xclang -disable-O0-optnone -g -emit-llvm -S

## -Xclang -disable-O0-optnone is important in order to not go crazy

OPT = /Users/andkakolyr/Desktop/LLVM/llvm-project/build/bin/opt
OPTFLAGS = -passes='indvars,loop-instr'

%.ll: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

%.stat: %.ll
	$(OPT) $(OPTFLAGS) $< -o $<

