LLVM = /home/andreas/llvm-project

CXX = $(LLVM)/build/bin/clang++
OPT = $(LLVM)/build/bin/opt
## llvm-project/build/bin/clang++ -Xclang -disable-O0-optnone -g -emit-llvm -S -I/opt/xilinx/xrt/include -w -I/tools/Xilinx/Vivado/2021.1/include -std=c++11 -fmessage-length=0 -L/opt/xilinx/xrt/lib -I/opt/Xilinx/Vitis_HLS/2020.2/include -lOpenCL -pthread  -lrt -lstdc++ dataset/rodinia_hls/backprop/backprop_kernel.cpp -o test.ll
## -Xclang -disable-O0-optnone is important in order to not go crazy
CXXFLAGS = -Xclang -disable-O0-optnone -g -emit-llvm -S
INCLUDE_FLAGS = -I/opt/xilinx/xrt/include -w -I/tools/Xilinx/Vivado/2021.1/include -std=c++11 -fmessage-length=0 -L/opt/xilinx/xrt/lib -I/opt/Xilinx/Vitis_HLS/2020.2/include -lOpenCL -pthread  -lrt -lstdc++
OPTFLAGS = -passes='instcombine,indvars,mem2reg,function(require<scalar-evolution>),function(require<loops>),loop-instr' -S

%.ll: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE_FLAGS) $< -o $@

%.stat: %.ll
	$(OPT) $(OPTFLAGS) $< -o $<

