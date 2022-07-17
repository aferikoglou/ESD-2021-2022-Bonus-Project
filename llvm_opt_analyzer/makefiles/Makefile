LLVM = /home/andreas/llvm-project

CXX = $(LLVM)/build/bin/clang++
CC = $(LLVM)/build/bin/clang
OPT = $(LLVM)/build/bin/opt
## llvm-project/build/bin/clang++ -Xclang -disable-O0-optnone -g -emit-llvm -S -I/opt/xilinx/xrt/include -w -I/tools/Xilinx/Vivado/2021.1/include -std=c++11 -fmessage-length=0 -L/opt/xilinx/xrt/lib -I/opt/Xilinx/Vitis_HLS/2020.2/include -lOpenCL -pthread  -lrt -lstdc++ dataset/rodinia_hls/backprop/backprop_kernel.cpp -o test.ll
## -Xclang -disable-O0-optnone is important in order to not go crazy
CXXFLAGS = -Xclang -disable-O0-optnone -g -emit-llvm -S

INCLUDE_FLAGS_CPP = -w -std=c++14 -fmessage-length=0 -lOpenCL -pthread  -lrt -lstdc++
INCLUDE_FLAGS_C = -w -fmessage-length=0 -pthread  -lrt
#INLUDE_FLAGS_OPENCL = -x cl -finclude-default-header -lOpenCL -w

XILINX_FLAGS = -I/opt/xilinx/xrt/include -I/tools/Xilinx/Vivado/2021.1/include -L/opt/xilinx/xrt/lib -I/opt/Xilinx/Vitis_HLS/2020.2/include

OPTFLAGS_COMMON = instcombine,indvars,mem2reg,function(require<scalar-evolution>),function(require<loops>)
OPTFLAGS_KSTAT = -passes='$(OPTFLAGS_COMMON),loop-instr' -S
OPTFLAGS_SSTAT = -passes='$(OPTFLAGS_COMMON),inlined-explorer' -S

%.llk: %.cpp
	$(CXX) -O0 $(CXXFLAGS) $(INCLUDE_FLAGS_CPP) $(XILINX_FLAGS) $< -o $@

%.llk: %.c
	$(CC) -O0 $(CXXFLAGS) $(INCLUDE_FLAGS_C) $(XILINX_FLAGS) $< -o $@

#%.llk: %.cl
#	$(CXX) -O0 $(CXXFLAGS) $(INLUDE_FLAGS_OPENCL) $(XILINX_FLAGS) $< -o $@

%.lls: %.cpp	
	$(CXX) -O1 $(CXXFLAGS) $(INCLUDE_FLAGS_CPP) $(XILINX_FLAGS) $< -o $@

%.lls: %.c
	$(CC) -O1 $(CXXFLAGS) $(INCLUDE_FLAGS_C) $(XILINX_FLAGS) $< -o $@

%.llp: %.cpp
	$(CXX) -O1 -disable-llvm-passes $(CXXFLAGS) $(INCLUDE_FLAGS_CPP) $(XILINX_FLAGS) $< -o $@

%.llp: %.c
	$(CC) -O1 -disable-llvm-passes $(CXXFLAGS) $(INCLUDE_FLAGS_C) $(XILINX_FLAGS) $< -o $@

#%.lls: %.cl	
#	$(CXX) -O1 $(CXXFLAGS) $(INLUDE_FLAGS_OPENCL) $(XILINX_FLAGS) $< -o $@

%.k_stat: %.llk
	$(OPT) $(OPTFLAGS_KSTAT) $< -o $<

%.s_stat: %.lls
	$(OPT) --inline --always-inline $< -o $<;
	$(OPT) $(OPTFLAGS_SSTAT) $< -o $<;

%.p_stat: %.llp
	$(OPT) -S -polly --polly-canonicalize --polly-prepare --polly-check-parallel --print-polyhedral-info $< -o $<;
