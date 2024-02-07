import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

subtraces = 17
if subtraces % 2 == 0 :
    rows = subtraces / 2
else :
    rows = (subtraces / 2) + 1
    
fig, ax = plt.subplots(int(rows), 2, figsize = (12,10))

k = 0


var_subtrace = []

for subtrace_n in range(subtraces) :

    filename1 = "Partition_traces_L1/w53-L1_read_" + str(subtrace_n) + ".csv"
    filename2 = "Partition_traces_L1/w53-L1_write_" + str(subtrace_n) + ".csv"
    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)
    
    df1.columns = ["ts"]
    df2.columns = ["ts"]
    
    read_rate = []
    
    
    #print(subtrace_n)
    
    df1['timestamp'] = pd.to_datetime(df1['ts'], unit='us')
    #print(df1.head())
    df2['timestamp'] = pd.to_datetime(df2['ts'], unit='us')
    #print(df2.head())
    
    if k > 1 :
        k = 0
    
    # Count occurrences every minute
    counts_per_minute_read = df1.groupby(pd.Grouper(key='timestamp', freq='1T')).size().tolist()
    counts_per_minute_write = df2.groupby(pd.Grouper(key='timestamp', freq='1T')).size().tolist()
    
    max_len_diff = abs(len(counts_per_minute_read) - len(counts_per_minute_write))
    
    if len(counts_per_minute_read) > len(counts_per_minute_write) :
        x = [0] * len(counts_per_minute_read)
        x[:len(counts_per_minute_write)] = counts_per_minute_write
        counts_per_minute_write = x
    else :
        x = [0] * len(counts_per_minute_write)
        x[:len(counts_per_minute_read)] = counts_per_minute_read
        counts_per_minute_read = x
       
    

    """
    # Display the counts per minute
    print("Counts per minute:", counts_per_minute_read)
    print("Counts per minute:", counts_per_minute_write)
    """
   # try:
    for n, r in enumerate(counts_per_minute_read) :
        try:
            read_rate.append(100 * round(r/(r + counts_per_minute_write[n]),2) )
        except ZeroDivisionError :
            read_rate.append(0)
        except IndexError :
            
            continue
    
    index = np.arange(len(read_rate))
    print("Subtrace Number :", subtrace_n)
    var_subtrace.append(np.round((np.sqrt(np.var(read_rate))/np.mean(read_rate)),4))
    print("Variance : ", np.var(read_rate))
    #plt.subplot(rows, 2, subtrace_n + 1)
    
    
    
    ax[int(subtrace_n/2) , k].plot(index, read_rate)
    ax[int(subtrace_n/2) , k].set_xlabel('Minutes in subtrace',  fontweight ='bold', fontsize=12) 
    ax[int(subtrace_n/2) , k].set_ylabel('prop of reads',     fontweight ='bold', fontsize=6) 
    """
    
    ax[int(subtrace_n/2) ].plot(index, read_rate)
    ax[int(subtrace_n/2) ].set_xlabel('Minutes in subtrace',  fontweight ='bold', fontsize=12) 
    ax[int(subtrace_n/2) ].set_ylabel('rate of arrivals',     fontweight ='bold', fontsize=12) 
    """
    k = k + 1
    
    #plt.plot(index , read_rate)
    #plt.xlabel("Minutes in subptrace")
    #plt.ylabel("Arrival proportion of reads")
       

    fig.tight_layout()
    plt.show()

    #plt.suptitle("For L1")
plt.savefig("read_ratio_w53_L1.png")
print("Printing coeff-variance by subtrace", var_subtrace)
