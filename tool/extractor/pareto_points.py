import AUX_pareto_optimizer as pareto
import json
import sys

parent_directory = sys.argv[1]
entries = sys.argv[2]
prefix = "DSE_EXPLORER"

optimizing_direction = (-1,-1,-1,-1,-1)

vector_list = []

for iter in range(int(entries)):
    try:
        res_list = []
        with open(f"{parent_directory}/{prefix}_{iter}/solution1/solution1_data.json",'r') as f:
            json_import = json.load(f)
        
            latency = int(json_import["ClockInfo"]["Latency"])
            period = float(json_import["ClockInfo"]["ClockPeriod"])

            res_list.append(latency*period/1000000)

            available = json_import['ModuleInfo']['Metrics']['krnl_KALMAN']['Area']


            for i in [available["UTIL_BRAM"],available["UTIL_DSP"],available["UTIL_FF"],available["UTIL_LUT"]]:
                if i[0]!= '~':
                    res_list.append(int(i))
                else:
                    res_list.append(0)


            go_ahead = True
            for x in res_list[1:]:
                if x > 100:
                    go_ahead = False
                    break
                    
            res_list.append(iter)

            if go_ahead:
                vector_list.append(list(res_list))
            #print(res_list)

    except:
        continue

opt = pareto.ParetoOptimizer(vector_list,optimizing_direction)
for x in opt.optimal_points():
    print(x)