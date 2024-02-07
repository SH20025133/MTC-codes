import pandas as pd


filename = "w53-SH-align64-sgdp7-iodepth16-clsize64-mtc.csv"
#filename = "w63-SH-iodepth1-clsize64-mtc-L1.csv"
df = pd.read_csv(filename)
df.columns = ['Q1','G1','D1','C1', 'Q2','G2','D2','C2', 'src']
#df.columns = ['Q', 'G', 'D', 'C', 'src']
print(df.head())

print("Count number of entries :", df.shape[0])

df_L1 = df[(df["src"] == 0) | (df["src"] == 1) | (df["src"] == 3)]
df_L1_read = df_L1[df_L1["src"] == 3]
df_L1_write = df_L1[(df_L1["src"] == 0) | (df_L1["src"] == 1)]
df_L1_read.drop(columns = ['Q2','G2','D2','C2', 'src'], inplace=True)
df_L1_write.drop(columns = ['Q2','G2','D2','C2', 'src'], inplace=True)
print(df_L1_read.head())

df_L2 = df[(df["src"] == 0) | (df["src"] == 2)]
df_L2_read = df_L2[df_L2["src"] == 2]
df_L2_write = df_L2[df_L2["src"] == 0]
df_L2_read.drop(columns = ['Q1','G1','D1','C1', 'src'], inplace=True)
df_L2_write.drop(columns = ['Q1','G1','D1','C1', 'src'], inplace=True)
print(df_L2_read.head())

df_L1_read.to_csv(filename.split(".")[0] + "-L1_read.csv", index = False)
df_L1_write.to_csv(filename.split(".")[0] + "-L1_write.csv", index = False)
df_L2_read.to_csv(filename.split(".")[0] + "-L2_read.csv", index = False)
df_L2_write.to_csv(filename.split(".")[0] + "-L2_write.csv", index = False)
"""

df_L1 = df[((df["C2"] == -1) & (df["C1"] != -1)) | ((df["C2"] != -1) & (df["C1"] != -1)) ]
df_L1.drop(columns = ['Q2','G2','D2','C2'], inplace=True)
df_L1.columns = ['Q','G','D','C', 'src']
print(df_L1.head())
print("Count number of L1s :", df_L1.shape[0])
df_L2 = df[((df["C1"] == -1) & (df["C2"] != -1)) | ((df["C2"] != -1) & (df["C1"] != -1)) ]
df_L2.drop(columns = ['Q1','G1','D1','C1'], inplace=True)
df_L2.columns = ['Q','G','D','C', 'src']
print(df_L2.head())
print("Count number of L2s :", df_L2.shape[0])

df_L1.to_csv(filename.split(".")[0] + "-L1.csv", index = False)
df_L2.to_csv(filename.split(".")[0] + "-L2.csv", index = False)


"""

"""
df_G1 = df_L1["G"]
df_G2 = df_L2["G"]

df_G = pd.concat([df_G1, df_G2]).sort_values(ascending = True)
print(df_G.head())
"""
"""
df3 = df[df.C1 == -1]
print(df3.head)
"""
