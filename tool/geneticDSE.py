import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.problem import starmap_parallelized_eval
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.factory import get_termination
from pymoo.optimize import minimize
import os
import multiprocessing
import subprocess
import json
import sys
import time
import psutil
from modules.annotator import Annotator
from modules.ds_explorator import RandomExplorer

from multiprocessing.pool import ThreadPool
from threading import Lock

my_env = os.environ.copy()

time_increment = 5 # 5 seconds
running_time = 3600 # 1 hour

METRICS_COUNT = 1 # LATENCY
RESOURCES_COUNT = 4 #BRAM, DSP, LUT, FF

#read code file and tcl script

input_file = sys.argv[1]
path_to_tcl = sys.argv[2]

#resources constraints

hls_annotator = Annotator()

lock = Lock()

n_threads = 40
pool = ThreadPool(n_threads)

i = 0
kill_count = 0

killed_array = np.array([0,101,101,101,101])

with open(input_file,'r') as iptf:
    hls_annotator.read_code(iptf)


hls_annotator.capture_datatypes(["DTYPE"])

hls_annotator.annotate_loops()
hls_annotator.annotate_arrays()
hls_annotator.update_limits()
n = 2*(hls_annotator.loop_counter + hls_annotator.array_counter)

def hls_synthesis(x):

    global i
    
    rand_dse = RandomExplorer(hls_annotator)
    rand_dse.get_genetic(x)
    rand_dse.get_instance()
    
    #...
    # RUN HLS
    
    lock.acquire()
    
    i+=1
    my_i = i
    file = open("iteration" + str(i) + ".cpp", "w+")

    for line in rand_dse.exploration_file.optimized_code:
        file.write(line)
    file.close()
    my_env['HLS_OPTIMIZER_PROJECT']=f'DSE_GENETIC_{i}'
    my_env['HLS_OPTIMIZER_INPUT_FILE']=f'iteration{i}.cpp'
    p = subprocess.Popen(['vitis_hls','-f',path_to_tcl],env=my_env)    
    
    lock.release()

    total_time = 0
    finished = False

    while (True):

        time.sleep(time_increment)
        #print(f"running for: {total_time}")
        total_time += time_increment
        if(total_time >= running_time or p.poll() != None):
            if(p.poll() != None): finished = True
            print(finished)
            pid = p.pid
            #print(f"Process {os.getpgid(pid)} running: {i.poll() != None}")
            try:
                
                for child in psutil.Process(pid).children(recursive=True):
                    child.kill()
                p.kill()
                kill_count = kill_count+1

            except:
                print("Either failed to terminate or already terminated")

            break

        
    # GET LATENCY AND RESOURSCES

    if(finished == False):
        return killed_array

    try:
        x = open(f'DSE_GENETIC_{my_i}/solution1/solution1_data.json','r')
    except:
        kill_count = kill_count+1
        return killed_array
    
    json_import = json.load(x)
        
    latency = int(json_import["ClockInfo"]["Latency"])
    period = float(json_import["ClockInfo"]["ClockPeriod"])

    latency = (latency*period)/1000000

    available = json_import['ModuleInfo']['Metrics']['krnl_KALMAN']['Area']
        
    x = available["UTIL_BRAM"]
    if x[0]!= '~':
        util_bram = int(x)
    else:
        util_bram = 0


    x = available["UTIL_DSP"]
    if x[0]!= '~':
        util_dsp = int(x)
    else:
        util_dsp = 0

    x = available["UTIL_FF"]
    if x[0]!= '~':
        util_ff = int(x)
    else:
        util_ff = 0

    x = available["UTIL_LUT"]
    if x[0]!= '~':
        util_lut = int(x)
    else:
        util_lut = 0


    return np.array([latency, util_dsp, util_bram, util_lut, util_ff])


class MyProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        super().__init__(n_var = n, n_obj = METRICS_COUNT, n_constr = RESOURCES_COUNT, xl = hls_annotator.lower_limit, xu = hls_annotator.upper_limit, **kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        
        f = hls_synthesis(x) # f = latency and resources, g = constraints for fpga resources limit

        g = f[1:5] - 100
        
        #g[0] = f[1] - resources[0] # DSP
        #g[1] = f[2] - resources[1] # BRAM
        #g[2] = f[3] - resources[2] # LUT
        #g[3] = f[4] - resources[3] # FF

        out["F"] = f
        out["G"] = g

problem = MyProblem(runner=pool.starmap, func_eval=starmap_parallelized_eval)

algorithm = NSGA2(
    pop_size=40,
    n_offsprings=40,
    sampling=get_sampling("int_random"),
    crossover=get_crossover("int_sbx", prob=0.9, eta=15),
    mutation=get_mutation("int_pm", eta=20),
    eliminate_duplicates=True
)

termination = get_termination("n_gen", 10)

res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True)

pool.close()

X = res.X
F = res.F

print(X)
print(F)

print(str(kill_count) + " syntheses were killed during execution")
