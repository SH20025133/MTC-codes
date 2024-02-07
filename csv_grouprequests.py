import pandas as pd
import numpy as np
import math
import os
import matplotlib.pyplot as plt


filename = "w53-SH-align64-sgdp7-iodepth16-clsize64-mtc_G.csv"
#action = "I"
df = pd.read_csv(filename)
df = df.reset_index(drop=True)

df.columns = ["ts"]
#df = df[df.action==action]

df1 = df["ts"]*10**-6
#df1 = df["ts"]
print(df)

start = df1[0]
#start = 4800
end = df1[len(df1.index)-1]
#end = df1.max()
i = num_arr = 0
j = 1
print("start",start)
print("end",end)

num_intervals = int(abs(start - end)/60)
print(num_intervals)

arr_rate = [] 
log_arr_rate = []
index = [] 
index_outlier = []

while(start <= end ):
    num_arr = 0
    while(df1[i] <= start + 60.0):
        num_arr = num_arr + 1
        i = i + 1
        if i > len(df1.index)-1:
            break;
    
    #print("Number of arrivals in ",j,"th interval is :",num_arr)
    #print(math.log(num_arr/60))
    arr_rate.append(round(num_arr/60,2)) 
    try :
        log_arr_rate.append((math.log(num_arr/60)))
    except ValueError :
        log_arr_rate.append(0)
    index.append(j)
    j += 1
    start +=60
#print(arr_rate.index(max(arr_rate)))

#print(arr_rate[41])


#Converting to csv

df3 = pd.DataFrame(np.array(arr_rate))



os.makedirs('CPD', exist_ok=True) 
df3.to_csv('CPD/w53-SH__min_without.csv',index=False)



