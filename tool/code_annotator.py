import sys
from annotator import Annotator

input_file = sys.argv[1]
Lines = []


input_FILE = ''

hls_annotator = Annotator()
with open(input_file,'r') as iptf:
    hls_annotator.read_code(iptf)


hls_annotator.capture_datatypes(["DTYPE"])
hls_annotator.annotate_loops()
hls_annotator.annotate_arrays()


print(hls_annotator.optimization_points_loops())
print(hls_annotator.optimization_points_arrays())
hls_annotator.pragma_insertion("LOOP_3",'loop',['some pragma','another_pragma','some other pragma'])

hls_annotator.print_code()
hls_annotator.finalize_code()


