import sys
from ...annotator import Annotator
from ...ds_explorator import RandomExplorer

input_file = sys.argv[1]
Lines = []


input_FILE = ''

hls_annotator = Annotator()
with open(input_file,'r') as iptf:
    hls_annotator.read_code(iptf)


hls_annotator.capture_datatypes(["DTYPE"])

hls_annotator.annotate_loops()
hls_annotator.annotate_arrays()

rand_dse = RandomExplorer(hls_annotator)
rand_dse.get_random()
rand_dse.get_instance()
rand_dse.exploration_file.print_code('final')
