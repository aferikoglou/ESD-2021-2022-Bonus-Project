import sys
import json
import subprocess
import os
import re
from LoopStatistics import LoopStat

def searchForLim(line,file,Llist):
    for item in Llist:
        if file in item.getLoopFilename():
            if item.getLoopLine() == line:
                return item.getLoopLimit()
    return 0

HLS_INPUT_FILE = sys.argv[1]
KERNEL_INFO_PRECURSOR = "hls_extracted_locs.txt"
CPP_AUTOGENERATED_FILE = 'hls_extractor_temp_file.cpp'
EXTRACTOR_OUTPUT_FILE = "extractor_output_file.out"
AUTOGEN = "autogen_exit"

DIRNAME,PLAIN_NAME = os.path.split(HLS_INPUT_FILE)
print(PLAIN_NAME)
if DIRNAME == "": DIRNAME = "."

KERNEL_INFO = f"{DIRNAME}/kernel_info.txt"

TGT_NO_EXT = HLS_INPUT_FILE.split(".")
STAT_FILE = PLAIN_NAME.split(".")[0] + ".k_stat"

LLVM_TEMP_FILE = "llvm_opt_pass_results.txt"
LLVM_ISA = "LLVM_InstructionSet.txt"

DELETE_LIST = [LLVM_TEMP_FILE,CPP_AUTOGENERATED_FILE,EXTRACTOR_OUTPUT_FILE,AUTOGEN]

if HLS_INPUT_FILE.split(".")[-1] == "cpp":
    LIBCLANG_COMPILATION_FLAGS = ["-I/opt/xilinx/xrt/include","-I/tools/Xilinx/Vivado/2021.1/include","-Wall","-O0","-g","-std=c++14","-fmessage-length=0","-L/opt/xilinx/xrt/lib","-I/opt/Xilinx/Vitis_HLS/2020.2/include","-lOpenCL","-pthread","-lrt","-lstdc++"]
else:
    LIBCLANG_COMPILATION_FLAGS = ["-I/opt/xilinx/xrt/include","-I/tools/Xilinx/Vivado/2021.1/include","-Wall","-O0","-g","-fmessage-length=0","-L/opt/xilinx/xrt/lib","-I/opt/Xilinx/Vitis_HLS/2020.2/include","-pthread","-lrt"]
LIBCLANG_COMPILATION_FLAGS = []

print("================ libclang parser =================\n")

#### input file parsing
p = subprocess.Popen(["./libclang_parser",HLS_INPUT_FILE,*LIBCLANG_COMPILATION_FLAGS])
p.wait()

file_lines = []
with open(HLS_INPUT_FILE,'r') as f:
    file_lines = f.readlines()

### action point extraction
with open(KERNEL_INFO_PRECURSOR,"r") as locs_file:
    locs_lines = locs_file.readlines()

loop_locs = []
array_locs = []
for i in locs_lines:
    tmp = i.split(',')

    line_loc = int(tmp[1])
    col_loc = int(tmp[2])
    global_idx = int(tmp[3])
    
    if tmp[0] == 'A':
        array_locs.append((line_loc,col_loc,global_idx,tmp[4][:-1]))
    elif tmp[0] == 'L':
        loop_locs.append((line_loc,col_loc,global_idx))

#### Array declaration analysis

array_decls = []
for line in array_locs:
    array_decl = re.split(r"[,;]",file_lines[line[0]][line[1]:-1])[0]
    dims = array_decl.count('[')
    expr_split = list(filter(lambda a: a!='',re.split(r"[\[\]]",array_decl)[1:]))
    array_decls.append((line[0],line[1],line[2],line[3],dims,*expr_split))


### Array sim file generation
with open(CPP_AUTOGENERATED_FILE,'w') as cpp_file:
    cpp_file.write(f"#include \"{HLS_INPUT_FILE}\"\n")
    cpp_file.write(f"#include <iostream>\n")
    cpp_file.write(f"using namespace std;\n\n")

    for decl in array_decls:
        for i in range(decl[4]):
            cpp_file.write(f"#define A_{decl[3]}_{i} {decl[5+i]}\n")

    cpp_file.write("int main(){\n")
    
    for decl in array_decls:
        for i in range(decl[4]):
            cpp_file.write(f"cout << \"A_{decl[3]}_{i}\" << ':' << A_{decl[3]}_{i} << endl;\n")

    cpp_file.write("return 0;\n}")

### Autogenerated file execution

p = subprocess.Popen(['make','-f',"makefiles/Makefile_Sim"])
p.wait()

with open(EXTRACTOR_OUTPUT_FILE,'w') as outfile:
    p = subprocess.Popen(['./autogen_exit'],stdout=outfile)
p.wait()

parser_lines = []
with open(EXTRACTOR_OUTPUT_FILE,'r') as infile:
    parser_lines = infile.readlines()

arrays_aux = dict()
arrays = dict()

################# EXTRACTED INFO ###############

for line in parser_lines:
    split_line = line.split(':')
    if line[0] == 'A':
        arrays_aux[split_line[0][2:]] = int(split_line[1])

for decl in array_decls:
    temp = []
    for i in range(decl[4]):
        temp.append(arrays_aux[f"{decl[3]}_{i}"])
    arrays[decl[3]] = list(temp)

for i in arrays:
    print(f"{i}, {arrays[i]}")

## annotate file
for L in loop_locs:
    file_lines[L[0]] = f"/*L{L[2]}:*/"+file_lines[L[0]]

for L in array_decls:
    file_lines[L[0]] = f"/*L{L[2]}:*/" +file_lines[L[0]]

enable_strip = 0

new_file_lines = []
if enable_strip > 0:

    for line in file_lines:
        if "#pragma" not in line: #pragma detected
            new_file_lines.append(line)
        else:
            if re.search(r'\barray_partition\b',line,flags=re.IGNORECASE)==None and re.search(r'\bpipeline\b',line,flags=re.IGNORECASE)==None and re.search(r'\bunroll\b',line,flags=re.IGNORECASE)==None:
                new_file_lines.append(line)

    with open(HLS_INPUT_FILE,'w') as outfile:
        outfile.writelines(new_file_lines)
else:
     with open(HLS_INPUT_FILE,'w') as outfile:
        outfile.writelines(file_lines)

print("============= LLVM opt Loop Analysis =============\n")

########## Run Clang + OPT pass ############
with open(LLVM_TEMP_FILE,"w") as llvm_tf:
    p = subprocess.Popen(["make","-f","makefiles/Makefile",f"{DIRNAME}/{STAT_FILE}"],stdout=llvm_tf)
    p.wait()

with open(LLVM_TEMP_FILE,'r') as llvm_tf:
    temp_lines = llvm_tf.readlines()

loop_analysis_results = []
for line in temp_lines:
    if "Filename," in line and PLAIN_NAME in line:
        loop_analysis_results.append(line[:-1])

############# Load Instruction / Opcode reference table ###############

with open(LLVM_ISA,"r") as llvm_isa_file:
    instr_list = llvm_isa_file.readlines()
instr_list = [x[:-1] for x in instr_list]

############## Results per Loop , generate JSON #####################
loopsAnalytical = []
for line in loop_analysis_results:
    t = LoopStat()
    t.loadFromString(line)
    loopsAnalytical.append(t)


#######################################################################
kernel_name = sys.argv[2]

with open(KERNEL_INFO,'w') as outfile:
    outfile.write(f"{kernel_name}\n")

    total_rng = len(array_decls) + len(loop_locs)
    for index in range(total_rng):
        for array in array_decls:
            if (index+1 == array[2]):
                array_str = f"L{array[2]},array,{array[3]}"
                for i in range(1,array[4]+1):
                    array_str += ',' + str(i) + ',' + str(arrays[array[3]][i-1])
                array_str += "\n"
                outfile.write(array_str)

        for loop in loop_locs:
            if (index+1 == loop[2]):
                loop_line = loop[0]
                loop_str = f"L{loop[2]},loop," + str(searchForLim(loop_line,PLAIN_NAME,loopsAnalytical)) + "\n"
                print(loop_str,end='')
                outfile.write(loop_str)

print("\nExported to kernel_info.txt\n")
### clean temp files
p = subprocess.Popen(["rm","-rf",*DELETE_LIST])