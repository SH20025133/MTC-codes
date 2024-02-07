import pandas as pd


filename = "w53-SH-align64-sgdp7-iodepth16-clsize64-mtc.csv"
#filename = "w63-SH-iodepth1-clsize64-mtc-L1.csv"
df = pd.read_csv(filename)
df.columns = ['Q1','G1','D1','C1', 'Q2','G2','D2','C2', 'src']
#df.columns = ['Q', 'G', 'D', 'C', 'src']
print(df.head())

#Extract G for cps

df_G0 = df[(df.src == 0) & (df.G1 != -1) ]
df_G0 = df_G0.G1
print(df_G0.head())
"""
df_G1 = df[(df.src == 1) & (df.G1 != -1) & (df.G2 != -1)]
df_G1 = df_G1.G1
#df_G1 = pd.concat([df_G1.G1, df_G1.G2])
print(df_G1.head())
"""
df_G2 = df[(df.src == 2) & (df.G2 != -1)]
df_G2 = df_G2.G2
print(df_G2.head())
df_G3 = df[(df.src == 3) & (df.G1 != -1)]
df_G3 = df_G3.G1
print(df_G3.head())

df_G =pd.concat([df_G0, df_G2, df_G3])*10**6
print(type(df_G))
df_G.sort_values(ascending = True)
print(df_G.head())
df_G.to_csv(filename.split(".")[0] +"_G.csv", index = False)
