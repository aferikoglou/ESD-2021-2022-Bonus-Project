import sys
import subprocess
from time import time,sleep
import os
import psutil

my_env = os.environ.copy()

path_to_script = sys.argv[1]
path_to_file = sys.argv[2]
path_to_tcl = sys.argv[3]
time_limit = int(sys.argv[4]) * 60 # for total execution
batch_runtime_limit = int(sys.argv[5]) * 60 # for each batch
threads = int(sys.argv[6])

def terminate_process(p_pid):
    process = psutil.Process(p_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def launch_process(name,iteration,environment,path_to_script,path_to_file,path_to_tcl):
    print(f"---> Launching iteration {iteration}")
    with open(f'iteration{iteration}.cpp','w+') as outfile:
        p = subprocess.Popen(['python3',path_to_script,path_to_file], stdout=outfile)
    p.wait()
    environment['HLS_OPTIMIZER_PROJECT']=f'{name}_{iteration}'
    environment['HLS_OPTIMIZER_INPUT_FILE']=f'iteration{iteration}.cpp'
    return subprocess.Popen(['vitis_hls','-f',path_to_tcl],env=environment)

print(f"total time: {time_limit}, process time limit {batch_runtime_limit}")

iter_counter = 0
process_dict = {}
start_time = time()
my_env['HLS_KERNEL_FUNCTION']='krnl_KALMAN'

for i in range(threads):
    process_dict[f"iteration_{iter_counter}"] = (launch_process('DSE_EXPLORER',iter_counter,my_env,path_to_script,path_to_file,path_to_tcl),time())
    iter_counter += 1

while ((time()-start_time) <= time_limit):
    for element in process_dict:
        if time()-process_dict[element][1] > batch_runtime_limit:
            terminate_process(process_dict[element][0].pid)
            del process_dict[element]
            process_dict[f"iteration_{iter_counter}"] = (launch_process('DSE_EXPLORER',iter_counter,my_env,path_to_script,path_to_file,path_to_tcl),time())
            iter_counter += 1
        elif process_dict[element][0].poll() != None:
            del process_dict[element]
            process_dict[f"iteration_{iter_counter}"] = (launch_process('DSE_EXPLORER',iter_counter,my_env,path_to_script,path_to_file,path_to_tcl),time())
            iter_counter += 1



for element in process_dict:
    terminate_process(process_dict[element][0].pid)    

print('======== >>>>>>> Finished <<<<<<<< =======')
