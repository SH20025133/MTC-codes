import pandas as pd
import numpy as np
import os

"""
To eliminate async writes comment out #85 and #131
"""
filename = "w87-SH-align64-sgdp7-iodepth1-clsize64-mtc.csv"

df = pd.read_csv(filename)
df.columns = ["Q1", "G1", "D1", "C1", "Q2", "G2", "D2", "C2", "src"]
#df = df[(df["I"] < df["C"]) & (df["I"] < df["D"]) & (df["D"] < df["C"])]
start = df['Q1'][0]
end = df['Q1'][len(df.index)-1]

print(start)
print(end)

df_src0 = pd.DataFrame()
df_src1 = pd.DataFrame()
df_src2 = pd.DataFrame()
df_src3 = pd.DataFrame()

start_updated = start

changepoint_BEAST = [1410]
changepoint_BEAST_mus = sorted([item*60 for item in changepoint_BEAST])

for df in pd.read_csv(filename, chunksize=1000000) :

    #df = pd.read_csv(filename)
    df.columns = ["Q1", "G1", "D1", "C1", "Q2", "G2", "D2", "C2", "src"]
    
    

    df_src0 = df_src0.append(df[(df["src"] == 0)], ignore_index=True)
    #print(df_src0.head())
    df_src1 = df_src1.append(df[(df["src"] == 1)], ignore_index=True)
    df_src2 = df_src2.append(df[(df["src"] == 2)], ignore_index=True)
    df_src3 = df_src3.append(df[(df["src"] == 3)], ignore_index=True)
    
    df_src0 = df_src0[(df_src0["G1"] < df_src0["C1"]) & (df_src0["G1"] < df_src0["D1"]) & (df_src0["D1"] <      df_src0["C1"])].reset_index(drop=True)
    df_src1 = df_src1[(df_src1["G1"] < df_src1["C1"]) & (df_src1["G1"] < df_src1["D1"]) & (df_src1["D1"] < df_src1["C1"]) & ((df_src1["C1"] - df_src1["D1"]) < (df_src1["G1"] < df_src1["C1"]))].reset_index(drop=True)
    df_src2 = df_src2[(df_src2["G2"] < df_src2["C2"]) & (df_src2["G2"] < df_src2["D2"]) & (df_src2["D2"] < df_src2["C2"]) & ((df_src2["C2"] - df_src2["D2"]) < (df_src2["G2"] < df_src2["C2"]))].reset_index(drop=True)
    df_src3 = df_src3[(df_src3["G1"] < df_src3["C1"]) & (df_src3["G1"] < df_src3["D1"]) & (df_src3["D1"] < df_src3["C1"]) & ((df_src3["C1"] - df_src3["D1"]) < (df_src3["G1"] < df_src3["C1"]))].reset_index(drop=True)
    
    
start0 = df_src0['Q1'][0]
start1 = df_src1['Q1'][0]
start2 = df_src2['Q2'][0]
start3 = df_src3['Q1'][0]

start_updated0 = start0
start_updated1 = start1
start_updated2 = start2
start_updated3 = start3



for item1 in changepoint_BEAST_mus:

        j = changepoint_BEAST_mus.index(item1)
        df1_src0 = df_src0[(df_src0['G1'] >= start_updated0) & (df_src0['G1'] <= start0 + item1)] 
        df1_src1 = df_src1[(df_src1['G1'] >= start_updated1) & (df_src1['G1'] <= start1 + item1)]
        df1_src2 = df_src2[(df_src2['G2'] >= start_updated2) & (df_src2['G2'] <= start2 + item1)]
        df1_src3 = df_src3[(df_src3['G1'] >= start_updated3) & (df_src3['G1'] <= start3 + item1)]
        #print(df1.head())

        #df = df[(df["I"] < df["C"]) & (df["I"] < df["D"]) & (df["D"] < df["C"])]
        start_updated0 = start0 + item1
        start_updated1 = start1 + item1
        start_updated2 = start2 + item1
        start_updated3 = start3 + item1

        print("***Printing for subtrace : ", j)

        #Computing mean response time for writes (src = 0)
        
        try : 

            Df_write_L1late = df1_src0[df1_src0["C1"] > df1_src0["C2"]]
            df_write =(Df_write_L1late.C1 - Df_write_L1late.Q1)
            Df_write_L1early = df1_src0[df1_src0["C1"] < df1_src0["C2"]]
            df_write = df_write.append(Df_write_L1early.C2 - Df_write_L1early.Q1)
            #df_write = df_write.append(df1_src1.C1 - df1_src1.Q1)
            df_write = pd.DataFrame(df_write, columns = ["RT"])
            df_write = df_write[df_write.RT < np.percentile(df_write.RT,100)]
            print("The mean response time for writes", df_write.mean()*10**6)

            #Computing mean response time for reads (src = 1,2,3)

            #df_read = (df1_src3.C1 - df1_src3.G1)*10**6 
            df_read_miss = (df1_src2.C2 - df1_src2.G2)
            df_read_hit = (df1_src3.C1 - df1_src3.G1)

            df_read_hit = pd.DataFrame(df_read_hit, columns = ["RT"])
            df_read_miss = pd.DataFrame(df_read_miss, columns = ["RT"])

            df_read_hit = df_read_hit[df_read_hit.RT < np.percentile(df_read_hit.RT,100)]
            df_read_miss = df_read_miss[df_read_miss.RT < np.percentile(df_read_hit.RT,100)]

            print("The mean response time for read hits", df_read_hit.mean()*10**6)
            print("The mean response time for read misses", df_read_miss.mean()*10**6)
        
        except IndexError :
            continue
        #os.makedirs('Partition_traces_', exist_ok=True)
        #df1.to_csv('Partition_traces_/w09-SH-iodepth1-clsize64-mtc_'+ str(j) +'.csv',index=False)

try :
        df1_src0 = df_src0[(df_src0['G1'] >= start_updated) & (df_src0['G1'] <= start + item1)] 
        df1_src1 = df_src1[(df_src1['G1'] >= start_updated) & (df_src1['G1'] <= start + item1)]
        df1_src2 = df_src2[(df_src2['G2'] >= start_updated) & (df_src2['G2'] <= start + item1)]
        df1_src3 = df_src3[(df_src3['G1'] >= start_updated) & (df_src3['G1'] <= start + item1)]
        
        print("df1_src0", df1_src0.head())
        print("df1_src1", df1_src1.head())
        print("df1_src2", df1_src2.head())
        print("df1_src3", df1_src3.head())
        
        print("***Printing for subtrace : ", j+1)

        #Computing mean response time for writes (src = 0)
        
       

        Df_write_L1late = df1_src0[df1_src0["C1"] > df1_src0["C2"]]
        df_write =(Df_write_L1late.C1 - Df_write_L1late.Q1)
        Df_write_L1early = df1_src0[df1_src0["C1"] < df1_src0["C2"]]
        df_write = df_write.append(Df_write_L1early.C2 - Df_write_L1early.Q1)
        #df_write = df_write.append(df1_src1.C1 - df1_src1.Q1)
        print("After src1", df_write.head(100))
        df_write = pd.DataFrame(df_write, columns = ["RT"])
        df_write = df_write[df_write.RT < np.percentile(df_write.RT,100)]
        print("The mean response time for writes", df_write.mean()*10**6)

        #Computing mean response time for reads (src = 1,2,3)

        #df_read = (df1_src3.C1 - df1_src3.G1)*10**6 
        #print("After src1", df_read.tail())
        df_read_miss = (df1_src2.C2 - df1_src2.G2)
        df_read_hit = (df1_src3.C1 - df1_src3.G1)

        df_read_hit = pd.DataFrame(df_read_hit, columns = ["RT"])
        df_read_miss = pd.DataFrame(df_read_miss, columns = ["RT"])

        df_read_hit = df_read_hit[df_read_hit.RT < np.percentile(df_read_hit.RT,100)]
        df_read_miss = df_read_miss[df_read_miss.RT < np.percentile(df_read_hit.RT,100)]

        print("The mean response time for read hits", df_read_hit.mean()*10**6)
        print("The mean response time for read misses", df_read_miss.mean()*10**6)

        



except IndexError :
        pass

#os.makedirs('Partition_traces_', exist_ok=True)
#df2.to_csv('Partition_traces_/w09-SH-iodepth1-clsize64-mtc_'+ str(j+1) +'.csv',index=False) 

