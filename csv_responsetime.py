import pandas as pd
import numpy as np
import statistics as st
from decimal import Decimal

i = 0
#for i in range(16) :
while i <= 16 :
    
   
    
    #filename1 = "Partition_traces_ST_L2/w09-SH-iodepth1-clsize64-mtc-L2_write_" + str(i) + ".csv"
    filename2 = "Partition_traces_ST_L2/w53-L2_read_ST_" + str(i) + ".csv"
    #filename = "Partition_traces_ST/w53-SH-iodepth4-L2_9.csv"
    
    #Df1 = pd.read_csv(filename1)
    #Df2 = pd.read_csv(filename2)
    #df = pd.concat([Df1, Df2], ignore_index = True)
    df = pd.read_csv(filename2)
    df.columns = ["I", "G", "D", "C"]
    #df[['Q', 'G', 'I', 'D', 'C']] = df[['Q', 'G', 'I', 'D', 'C']].apply(pd.to_numeric)

    """
    filename2 = "w11-SH-L2_all_testing2.csv"
    df2 = pd.read_csv(filename2)
    df2.columns = ["sector","I","D","C"]
    """
    print("Printing :", filename2)
    response_time = []
    df1 = (df.C - df.I)*10**6
    response_time = df1.to_numpy()
    #mean_response_time = np.nanmean(response_time)

    #print("The average response time is: ",mean_response_time)

    df2 = (df.C - df.D)*10**6
    service_time = df2.to_numpy()
    #mean_service_time = np.nanmean(service_time)

    df3 = df[(df["I"] < df["C"]) & (df["I"] < df["D"]) & (df["D"] < df["C"])]*10**6
    df3 = df['I']*10**6
    print(type(df3))
    df3 = pd.DataFrame(df3)
    df3.columns = ["ts_us"]
    df3 = df3.sort_values(by = ["ts_us"])
    df3 = df3["ts_us"].diff()
    #df3.diff()
    """
    df3 = pd.DataFrame(df3)
    df3.columns = ["IAT"]
    #print(df3.head())
    df3 = df3[df3["IAT"] > 0]
    df3 = df3.reset_index()
    """
    IAT = df3.to_numpy()
    
    if(any(service_time>response_time)): 
        c = np.where(service_time>response_time)[0]
        print(np.where(service_time>response_time)[0])
    else :
        c = []

    service_time = list(service_time)
    response_time = list(response_time)
    IAT = list(IAT)

    k = 0

    for i in c:
        print(i)

        service_time.pop(i - k)
        response_time.pop(i - k)
        IAT.pop(i - k)
        k += 1

    service_time = np.array(service_time)
    response_time = np.array(response_time)

    print(max(service_time))
    print(max(response_time))
    mean_response_time = np.nanmean(response_time)
    print("The average response time is: ",mean_response_time)

    mean_service_time = np.nanmean(service_time)
    print("The average service time is: ",mean_service_time)

    mean_IAT = np.nanmean(IAT)
    print("The average IAT is: ")
    print('%.2E' % Decimal(mean_IAT))
    
    print("Load factor : ", mean_service_time/mean_IAT)
    i += 1
