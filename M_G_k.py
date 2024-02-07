"""
This code will have two parts inside M/G/1 where

-G (let G1) is a H2 distribution as rexp(r) + wexp(w)
-G (let G2)is a combination of two H2's in the proportion of r and w


The only line you'll change for read-only and write-only is #110 as calcmeanreadH2 for reads or calcmeanwriteH2 for writes
allfitw09-SH-iodepth1-clsize64-mtc-L1(week).csv
"""

import pandas as pd
import math

inp_fn = "allfitw46-SH-iodepth1-clsize64-mtc-L2"
df_iat = pd.read_csv(inp_fn+".csv")
df_iat1 = df_iat
df_st = pd.read_csv(inp_fn+"_ST.csv")
#f_out = open(inp_fn+".csv","w")

df_exp_iat = df_iat[df_iat.DistName == "exponential"]
df_exp_st = df_st[df_st.DistName == "hyperexp"]

rwprop = [(.1727, 1-.1727), (.0025, 1-.0025), (.0005, 1-.0005), (0,  1-0), (.0338, 1-.0338), (.0011, 1-.0011), (0, 1-0), (.0015, 1-.0015), (0, 1-0), (0, 1-0), (.1139, 1-.1139), (.4766, 1-.4766), (0, 1-0), (.0001, 1-.0001)]
print("Length of rwprop", len(rwprop))
subtrace = 0
r_line = ""


while subtrace <= 12 :
    
    lam_values = []
    mu_values = []
    
    df_exp_subtrace_iat_read = df_exp_iat[df_exp_iat.fname.str.contains("_read_"+str(subtrace))]
    df_exp_subtrace_iat_write = df_exp_iat[df_exp_iat.fname.str.contains("_write_"+str(subtrace))]
    df_exp_subtrace_st_read = df_exp_st[df_exp_st.fname.str.contains("_read_ST_"+str(subtrace))]
    df_exp_subtrace_st_write = df_exp_st[df_exp_st.fname.str.contains("_write_ST_"+str(subtrace))]
    
    
    lam_values.append(1/df_exp_subtrace_iat_read.Params_1.values[0])
    lam_values.append(1/df_exp_subtrace_iat_write.Params_1.values[0])
    
    #mu_values = [mu1, mu2, p, mu3, mu4, q]
    
    mu_values.append(1/df_exp_subtrace_st_read.Params_1.values[0])
    mu_values.append(1/df_exp_subtrace_st_read.Params_2.values[0])
    mu_values.append(df_exp_subtrace_st_read.Params_3.values[0])
    
    mu_values.append(1/df_exp_subtrace_st_write.Params_1.values[0])
    mu_values.append(1/df_exp_subtrace_st_write.Params_2.values[0])
    mu_values.append(df_exp_subtrace_st_write.Params_3.values[0])
    
    print(len(mu_values))
    #print("Lambda", lam_values)
    #print("Mu", mu_values)
        
      
    #rwprop[subtrace]
    #lam_values = [1/152946.7752, 1/185224.2223]
    lam = lam_values[0] + lam_values[1]
    #mu_values = [1/1000.983528, 1/254.6689582]

    #print(lam_values, mu_values, rwprop[subtrace])

    #Calculate mean H2
    
    def calcmeanreadH2(mu_values) :
        
        ES = mu_values[2] / mu_values[0] + (1 - mu_values[2]) / mu_values[1]
        #print("*",ES)
        return ES
    
    def calcmeanwriteH2(mu_values) :
        
        ES = mu_values[5] / mu_values[3] + (1 - mu_values[5]) / mu_values[3]
        #print("*",ES)
        return ES
    
    #Calculate E[S]

    def calcS(mu_values, rwprop) :
        ES_1 = (mu_values[2]/mu_values[0] + (1-mu_values[2])/mu_values[1]) * rwprop[0]
        ES_2 = (mu_values[5]/mu_values[3] + (1-mu_values[5])/mu_values[4]) * rwprop[1]
        #print("*",ES)
        return ES_1 + ES_2

    print("Mean service time in us", calcS(mu_values, rwprop[subtrace]))

    #Calculate E[S^2]

    def calcS2(mu_values, rwprop) :
        
        ES2_1 = 2 * (mu_values[2]/(mu_values[0]**2) + (1-mu_values[2])/(mu_values[1]**2)) * rwprop[0]
        ES2_2 = 2 * (mu_values[5]/(mu_values[3]**2) + (1-mu_values[5])/(mu_values[4]**2)) * rwprop[1]
        #print("**",ES2)
        return ES2_1 + ES2_2
    
    #print("Mean squared service time in us", calcS2(mu_values, rwprop[subtrace]))

    rho = lam * calcS(mu_values, rwprop[subtrace])
    print("Load factor", rho)
    
    #Calculate the coeff of variance for service time distribution
    def calc_coeffvar_service(rwprop, mu_values) :

        ES = rwprop[0] / mu_values[0] + rwprop[1] / mu_values[1]
        ES2 = 2 * (rwprop[0] / (mu_values[0]**2) + rwprop[1] / (mu_values[1]**2))

        return (math.sqrt(ES2/(ES**2) - 1)), ES

    #Calculate the response time for M/G/k

    k = 2

    coeff_var, mean_serv = calc_coeffvar_service(rwprop[subtrace], mu_values)

    #calculate wait time in queue Wq
    #calc_variance = calcS2(mu_values, rwprop[subtrace]) - calcS(mu_values, rwprop[subtrace])**2

    Wq = (lam * calcS2(mu_values, rwprop[subtrace])) / 2 * (1 - rho)
    Wq = Wq * (math.pow(coeff_var,2) + 1)/2
    W = Wq + calcmeanwriteH2(mu_values)
    
    #Lq = ((lam**2)*calc_variance + rho**2) / 2 * (1 - rho)

    print("For subtrace_", subtrace)
    print("Waiting time in queue",Wq)
    print("Response time",W)
    
    subtrace = subtrace + 1
