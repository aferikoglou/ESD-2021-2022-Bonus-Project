import sys
import re

IN_FILE = sys.argv[1]

with open(IN_FILE,"r") as hlsinf:
    f_lines = hlsinf.readlines()

new_lines = []
for line in f_lines:
    if "#pragma" not in line: #pragma detected
        new_lines.append(line)
    else:
        if re.search(r'\barray_partition\b',line,flags=re.IGNORECASE)==None and re.search(r'\bpipeline\b',line,flags=re.IGNORECASE)==None and re.search(r'\bunroll\b',line,flags=re.IGNORECASE)==None:
            new_lines.append(line)

with open(IN_FILE,'w') as outfile:
    outfile.writelines(new_lines)
