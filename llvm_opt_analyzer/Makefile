CXX = /Users/andkakolyr/Desktop/LLVM/llvm-project/build/bin/clang++
CXXFLAGS = -O0 -Xclang -disable-O0-optnone -g -emit-llvm -S

## -Xclang -disable-O0-optnone is important in order to not go crazy

OPT = /Users/andkakolyr/Desktop/LLVM/llvm-project/build/bin/opt
OPTFLAGS = --passes=fn_analyze -disable-output

%.ll: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

%.stat: %.ll
	$(OPT) $(OPTFLAGS) $<

