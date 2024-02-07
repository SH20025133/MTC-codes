import pandas as pd
import time
import numpy as np
import os
pd.options.display.float_format = '{:,.8f}'.format

cp_index = 16    
#w09-SH-iodepth1-clsize64-mtc-L2_read_0.csv
#while i <= 4 :
for i in range(cp_index + 1) :
    
    filename = "Partition_traces_ST_L2/w53-L2_read_ST_" + str(i) + ".csv"

    print("Reading CSV...",end="",flush=True)
    df = pd.read_csv(filename)
    print(u'\u2713')
    
    df = df.reset_index(drop=True)
    df.columns = ["Q","G","D","C"]
    #df[['Q', 'G', 'I', 'D', 'C']] = df[['Q', 'G', 'I', 'D', 'C']].apply(pd.to_numeric)
    print(df.head())
    
   
    df1 = (df.C - df.D)*10**6
    
    os.makedirs('Partition_traces_ST_L2', exist_ok=True)
    df1.to_csv('Partition_traces_ST_L2/w53-L2_read_ST_'+ str(i) +'_out.csv',index=False)
    i += 1
