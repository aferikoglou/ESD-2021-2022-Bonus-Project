import json
import sys

iterations  = int(sys.argv[1])
name = 'DSE_EXPLORER'

best_latency = (-1,10**17)

for i in range(iterations):
    try:
        x = open(f'{name}_{i}/solution1/solution1_data.json','r')
        print("File Opened")
        json_import = json.load(x)
        
        latency = int(json_import["ClockInfo"]["Latency"])
        period = float(json_import["ClockInfo"]["ClockPeriod"])

        available = json_import['ModuleInfo']['Metrics']['krnl_KALMAN']['Area']
        #print("Json Imported")
        #print(available)
        

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

        x = available["UTIL_URAM"]
        if x[0]!= '~':
            util_uram = int(x)
        else:
            util_uram = 0

        print("Data Gathered")


        if (util_bram < 100 and util_dsp < 100 and util_ff < 100 and util_lut < 100 and util_uram < 100):
            ttime = latency * period / 1000000
            print(f'iteration {i} available, latency {ttime} ms')
            if ttime < best_latency[1]:
                best_latency = (i,ttime)

        
    except:
        print(f"failed")

print(f"\n\n >>>> Best valid result for iteration {best_latency[0]}, latency: {best_latency[1]} ms\n\n")
        

