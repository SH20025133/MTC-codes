import pandas as pd

trace = ["L1","L2"]
nature = ["read", "write"]
action = ['Q1','Q2']


for trace_n in trace :
    for nature_n in nature :
        
        action_index = trace.index(trace_n)
        action_n = action[action_index]
        filename = "w64-SH-align64-sgdp7-iodepth16-clsize64-mtc-" + trace_n + "_" + nature_n + ".csv"
        print(filename)
        
        df = pd.read_csv(filename)
        df = df[action_n]*10**6
        
        df.to_csv(filename.split(".")[0]+"_"+action_n+".csv", index = False, header=False)


