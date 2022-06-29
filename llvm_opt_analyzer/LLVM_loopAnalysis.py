import sys
import json
import subprocess
import os

TGT_SRC = sys.argv[1]
PLAIN_NAME = os.path.split(TGT_SRC)[1]
TGT_NO_EXT = TGT_SRC.split(".")[0]
LLVM_TEMP_FILE = "llvm_opt_pass_results.txt"
LLVM_ISA = "LLVM_InstructionSet.txt"
print("============= LLVM Loop Analysis =================\n")

########## Run Clang + OPT pass ############
with open(LLVM_TEMP_FILE,"w") as llvm_tf:
    p = subprocess.Popen(["make",f"{TGT_NO_EXT}.stat"],stdout=llvm_tf)
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

#######################################################################

############## Results per Loop #####################

line_results = []
for line in loop_analysis_results:
    line_dict = dict()
    temp = line.split("|")
    for item in temp:
        comma_split = item.split(",")
        line_dict[comma_split[0]] = comma_split[1] if len(comma_split) == 2 else comma_split[1:]
    line_results.append(dict(line_dict))

for line in line_results:
    line["LoopLim"] = int(line["LoopLim"]) - 1 
    line["VectorizationHint"] = True if line["VectorizationHint"] == '1' else False
    print(line)



    


        












