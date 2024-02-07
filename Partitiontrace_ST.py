import pandas as pd
import numpy as np
import os

filename = "w53-SH-align64-sgdp7-iodepth16-clsize64-mtc-L2_read.csv"

df = pd.read_csv(filename)
df.columns = ["I", "G", "D", "C"]
df = df[(df["I"] < df["C"]) & (df["I"] < df["D"]) & (df["D"] < df["C"])]
start = df['I'][0]
end = df['I'][len(df.index)-1]
print(df)
print(start)
print(end)

start_updated = start

changepoint_BEAST = [458.0, 502.0, 557.0, 655.0, 680.0, 722.0, 809.0, 849.0, 1115.0, 1189.0, 1295.0, 1352.0, 1453.0, 1517.0, 1789.0, 1855.0]
changepoint_BEAST_mus = sorted([item*60 for item in changepoint_BEAST])


for item1 in changepoint_BEAST_mus:
    
        j = changepoint_BEAST_mus.index(item1)
        df1 = df[(df['I'] >= start_updated) & (df['I'] <= start + item1)] 
        #print(df1.head())
        start_updated = start + item1
        os.makedirs('Partition_traces_ST_L2', exist_ok=True)
        df1.to_csv('Partition_traces_ST_L2/w53-L2_read_ST_'+ str(j) +'.csv',index=False)

try :
        df2 = df[(df['I'] > start + changepoint_BEAST_mus[-1]) & (df['I'] <= end)] 
        
        
        
except IndexError :
        pass
        
os.makedirs('Partition_traces_ST_L2', exist_ok=True)
df2.to_csv('Partition_traces_ST_L2/w53-L2_read_ST_'+ str(j+1) +'.csv',index=False) 

