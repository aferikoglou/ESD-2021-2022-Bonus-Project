import sys
import subprocess
from time import time,sleep
import os
import signal
import psutil

my_env = os.environ.copy()

path_to_script = sys.argv[1]
path_to_file = sys.argv[2]
path_to_tcl = sys.argv[3]
time_limit = int(sys.argv[4]) * 60 # for total execution
batch_runtime_limit = int(sys.argv[5]) * 60 # for each batch
batch_size = int(sys.argv[6])

def terminate_process(p_pid):
    process = psutil.Process(p_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


print(f"total time: {time_limit}, batch time limit {batch_runtime_limit}")

batch_counter = 0
process_list = []
start_time = time()

time_increment = 5


my_env['HLS_KERNEL_FUNCTION']='krnl_KALMAN'

while True:
    if (time()-start_time) >= time_limit:
        break

    for i in range(batch_counter,batch_counter+batch_size):
        with open(f'iteration{i}.cpp','w+') as outfile:
            process_list.append(subprocess.Popen(['python3',path_to_script,path_to_file], stdout=outfile))

    for x in process_list:
        x.wait()

    process_list = []
    for i in range(batch_counter,batch_counter+batch_size):
        my_env['HLS_OPTIMIZER_PROJECT']=f'DSE_EXPLORER_{i}'
        my_env['HLS_OPTIMIZER_INPUT_FILE']=f'iteration{i}.cpp'
        process_list.append(subprocess.Popen(['vitis_hls','-f',path_to_tcl],env=my_env))

    batch_run_time = 0
    while batch_run_time <= batch_runtime_limit:
        
        batch_run_time += time_increment
        all_finished = True
        for i in process_list:
            all_finished &= (i.poll() != None)
        print(f"time:{batch_run_time}, finished:{all_finished}")
        if all_finished:
            break
        sleep(time_increment)

    for i in process_list:
        pid = i.pid
        #print(f"Process {os.getpgid(pid)} running: {i.poll() != None}")
        try:
            print(f">>> Terminating offending process: {os.getpgid(pid)} <<<")
            terminate_process(pid)
        except:
           print("Either failed to terminate of already terminated")

    batch_counter += batch_size
    print("Ready for new batch")

print('======== >>>>>>> Finished <<<<<<<< =======')
