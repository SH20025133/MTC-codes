"""
This code will have two parts inside M/G/1 where

-G (let G1) is a H2 distribution as rexp(r) + wexp(w)
-G (let G2)is a combination of two H2's in the proportion of r and w

allfitw64-SH-iodepth1-clsize64-mtc-L1.xls   allfitw64-SH-iodepth1-clsize64-mtc-L1_ST.xls
The only line you'll change for read-only and write-only is #92 as mu_values[0] for reads or mu_values[1] for writes
allfitw46-SH-iodepth1-clsize64-mtc-L1.csv
"""

import pandas as pd
import math

inp_fn = "allfitw87-SH-iodepth1-clsize64-mtc-L2"
df_iat = pd.read_csv(inp_fn+".csv")
df_iat1 = df_iat
df_st = pd.read_csv(inp_fn+"_ST.csv")
df_st1 = df_st
#f_out = open(inp_fn+".csv","w")

df_exp_iat = df_iat[df_iat.DistName == "exponential"]
df_exp_st = df_st[df_st.DistName == "exponential"]

"""
rwprop = [(.0049, 1-.0049), (.2283, 1-.2283), (.9586, 1-.9586), (.7460,  1-.7460), (.9754, 1-.9754), (.0001, 1-.0001), (.0001, 1-.0001), (0, 1-0), (.0177, 1-.0177), (.0006, 1-.0006), (.0001, 1-.0001), (.0004, 1-.0004), (0, 1-0), (.0087, 1-.0087), (0, 1-0), (0, 1-0)]
"""

rwprop = [(.1175, 1-.1175)]
print("Length of rwprop", len(rwprop))
subtrace = 0
r_line = ""


while subtrace < 1 :
    
    lam_values = []
    mu_values = []
    
    
    
    df_exp_subtrace_iat_read = df_exp_iat[df_exp_iat.fname.str.contains("_read_"+str(subtrace))]
    df_exp_subtrace_iat_write = df_exp_iat[df_exp_iat.fname.str.contains("_write_"+str(subtrace))]
    df_exp_subtrace_st_read = df_exp_st[df_exp_st.fname.str.contains("_read_ST_"+str(subtrace))]
    df_exp_subtrace_st_write = df_exp_st[df_exp_st.fname.str.contains("_write_ST_"+str(subtrace))]
    
    """
    print(df_exp_subtrace_iat_read.head())
    print(df_exp_subtrace_iat_write.head())
    print(df_exp_subtrace_st_read.head())
    print(df_exp_subtrace_st_write.head())
    """
    
    lam_values.append(1/df_exp_subtrace_iat_read.Params_1.values[0])
    lam_values.append(1/df_exp_subtrace_iat_write.Params_1.values[0])
    
    #print(df_exp_subtrace_st_read.Params_1.values)
    mu_values.append(1/df_exp_subtrace_st_read.Params_1.values[0])
    mu_values.append(1/df_exp_subtrace_st_write.Params_1.values[0])
    print(len(mu_values))
        
      
    #rwprop[subtrace]
    #lam_values = [1/152946.7752, 1/185224.2223]
    lam = lam_values[0] + lam_values[1]
    #mu_values = [1/1000.983528, 1/254.6689582]

    #print(lam_values, mu_values, rwprop[subtrace])

    #Calculate E[S]

    def calcS(mu_values, rwprop) :
        ES = rwprop[0] / mu_values[0] + rwprop[1] / mu_values[1]
        #print("*",ES)
        return ES

    print("Mean service time in us", calcS(mu_values, rwprop[subtrace]))

    #Calculate E[S^2]

    def calcS2(mu_values, rwprop) :
        ES2 = 2 * (rwprop[0] / (mu_values[0]**2) + rwprop[1] / (mu_values[1]**2))
        #print("**",ES2)
        return ES2

    print("For subtrace_", subtrace)
    
    rho = lam * calcS(mu_values, rwprop[subtrace])
    print("Load factor", rho)
    
    rho2 = lam * (mu_values[0] + mu_values[1])
    print("Actual Load factor", rho2)



    #calculate wait time in queue Wq
    calc_variance = calcS2(mu_values, rwprop[subtrace]) - calcS(mu_values, rwprop[subtrace])**2

    Wq = (lam * calcS2(mu_values, rwprop[subtrace])) / 2 * (1 - rho)
    W = Wq + 1 / mu_values[0]
    Lq = lam * Wq
    #Lq = ((lam**2)*calc_variance + rho**2) / 2 * (1 - rho)

    
    print("Waiting time in queue",Wq)
    print("Response time",W)
    
    subtrace = subtrace + 1
