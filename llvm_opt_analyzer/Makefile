###################################
# Configuring the Makefile
###################################
# 1. Set CXX as the path to the clang++ compiler
# 2. Set OPT as the path to the llvm/opt optimizer
# 3. Set INCLUDE_FLAGS to include any necessary header files and other info, modify according to your system
###################################

# To run opt pass: make </path/to/source/file>.stat
# e.g: make bubble_sort.stat

# ############# Notes #############
# 1. Compiling with -O0 for now. Optimizations change the structure of the code and mess up debug info as a result.
# 	We will deal with that later
# 2. "-Xclang -disable-O0-optnone" flags are NECESSARY. When compiling with -O0 clang++ marks the source code to not
#	be processed by opt (optnone). WE WANT OPT TO PROCESS THE CODE. 
# 3. Our custom pass is named 'loop-instr'. This is the argument given to opt as -passes='loop-instr'
###################################

CXX = /Users/andkakolyr/Desktop/LLVM/llvm-project/build/bin/clang++
CXXFLAGS = -O0 -Xclang -disable-O0-optnone -g -emit-llvm -S
OPT = /Users/andkakolyr/Desktop/LLVM/llvm-project/build/bin/opt 
OPTFLAGS = -passes='instcombine,indvars,mem2reg,function(require<scalar-evolution>),function(require<loops>),loop-instr' -S
#OPTFLAGS_OLD = -enable-new-pm=0 -scalar-evolution -S

# The following line is disabled as the necessary files are not installed on my current machine.
#INCLUDE_FLAGS = -I/opt/xilinx/xrt/include -w -I/tools/Xilinx/Vivado/2021.1/include -std=c++11 -fmessage-length=0 -L/opt/xilinx/xrt/lib -I/opt/Xilinx/Vitis_HLS/2020.2/include -lOpenCL -pthread  -lrt -lstdc++

.PRECIOUS: %.ll

%.ll: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

%.stat: %.ll
	$(OPT) $(OPTFLAGS) $< -o $<

