import pandas as pd
import numpy as np
import math
import os

#filename = "w09_L2.csv"
filename = "w53-SH-align64-sgdp7-iodepth16-clsize64-mtc-L2_read_Q2.csv"

print(filename)
df = pd.read_csv(filename)
df = df.reset_index(drop=True)
df.columns = ["ts"]
#df = df[df.action==action]

df_new = df["ts"]
start = df_new[0]
end = df_new[len(df_new.index)-1]
arr_new = pd.Series(df_new.to_numpy())

#BEAST cpd
changepoint_BEAST = [458.0, 502.0, 557.0, 655.0, 680.0, 722.0, 809.0, 849.0, 1115.0, 1189.0, 1295.0, 1352.0, 1453.0, 1517.0, 1789.0, 1855.0]
#changepoint_BEAST = [ 953.0, 974.0, 1020.0, 1130.0, 1196.0, 1222.0, 1250.0, 1263.0, 1284.0, 1311.0]
changepoint_BEAST_mus = sorted([item*60*10**6 for item in changepoint_BEAST])
#changepoint_BEAST_mus = changepoint_BEAST_mus.sort()
print(df_new[1])
print(changepoint_BEAST_mus)
print(start + changepoint_BEAST_mus[0])

#Extracting subtraces

start_updated = start
row = 0


for item1 in changepoint_BEAST_mus:
    j = changepoint_BEAST_mus.index(item1)
    df_sub = pd.DataFrame()
    row_sub = 0
    #print(item1,start + item1)
    sub_arr = np.array([])
    
    """
    while (start_updated <= start + item1):
            
            sub_arr = np.append(sub_arr , arr_new[row])
            #print(arr_new[row])
            start_updated = arr_new[row]
            row += 1
    """
    sub_arr = arr_new[(arr_new > start_updated) & (arr_new <= start + item1)]
    print(row)
    print(start_updated)
    start_updated = start + item1        
    #start = start_updated
    sub_df = pd.DataFrame(sub_arr)
    os.makedirs('Partition_traces_L2', exist_ok=True)
    sub_df.to_csv('Partition_traces_L2/w53-L2_read_'+ str(j) +'.csv',index=False) 

last_array =  np.array([])
last_df = pd.DataFrame()
try :
        last_array = arr_new[(arr_new > start + changepoint_BEAST_mus[-1]) & (arr_new <= end)]
        print(row)
        
except IndexError :
        pass
        
last_df = pd.DataFrame(last_array)
last_df.to_csv('Partition_traces_L2/w53-L2_read_'+ str(j+1) +'.csv',index=False) 
print("****",last_df)
"""
while start + changepoint_BEAST_mus[-1] <= end :
    try :
        last_array = np.append(last_array , arr_new[row])
        row += 1
        start_updated = arr_new[row]
    except IndexError :
        break
print(row)
last_df = pd.DataFrame(last_array)
last_df.to_csv('Partition_traces/w11-SH-L2_'+ str(j+1) +'.csv',index=False) 

"""
    
  
        
