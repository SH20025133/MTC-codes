"""
This code will have two parts inside M/G/1 where

-G (let G1) is a H2 distribution as rexp(r) + wexp(w)
-G (let G2)is a combination of two H2's in the proportion of r and w

allfitw64-SH-iodepth1-clsize64-mtc-L1.xls   allfitw64-SH-iodepth1-clsize64-mtc-L1_ST.xls
The only line you'll change for read-only and write-only is #81 as mu_values[0] for reads or mu_values[1] for writes
allfitw09-SH-iodepth1-clsize64-mtc-L1(week).csv
"""

import pandas as pd
import math

inp_fn = "allfitw46-SH-iodepth1-clsize64-mtc-L1"
df_iat = pd.read_excel(inp_fn+".xls")
df_iat1 = df_iat
df_st = pd.read_excel(inp_fn+"_ST.xls")
#f_out = open(inp_fn+".csv","w")

df_exp_iat = df_iat[df_iat.DistName == "exponential"]
df_exp_st = df_st[df_st.DistName == "exponential"]

rwprop = [(.1863, 1-.1863), (.1755, 1-.1755), (.3362, 1-.3362), (.1042,  1-.1042), (.1991, 1-.1991), (.0395, 1-.0395), (.1127, 1-.1127), (.0813, 1-.0813), (.3707, 1-.3707), (.0133, 1-.0133), (0, 1-0), (.4766, 1-.4766), (.5134, 1-.5134), (.2535, 1-.2535)]
print("Length of rwprop", len(rwprop))
subtrace = 1
r_line = ""


while subtrace <= 13 :
    
    lam_values = []
    mu_values = []
    
    df_exp_subtrace_iat_read = df_exp_iat[df_exp_iat.fname.str.contains("_read_"+str(subtrace))]
    df_exp_subtrace_iat_write = df_exp_iat[df_exp_iat.fname.str.contains("_write_"+str(subtrace))]
    df_exp_subtrace_st_read = df_exp_st[df_exp_st.fname.str.contains("_read_ST_"+str(subtrace))]
    df_exp_subtrace_st_write = df_exp_st[df_exp_st.fname.str.contains("_write_ST_"+str(subtrace))]
    
    
    lam_values.append(1/df_exp_subtrace_iat_read.Params_1.values[0])
    lam_values.append(1/df_exp_subtrace_iat_write.Params_1.values[0])
    
    mu_values.append(1/df_exp_subtrace_st_read.Params_1.values[0])
    mu_values.append(1/df_exp_subtrace_st_write.Params_1.values[0])
    mu = mu_values[0] + mu_values[1]
    print(len(mu_values))
        
      
    #rwprop[subtrace]
    #lam_values = [1/152946.7752, 1/185224.2223]
    lam = lam_values[0] + lam_values[1]
    #mu_values = [1/1000.983528, 1/254.6689582]

    #Calculate the M/M/k waiting(or delay) time
    
    def waiting_MMk(lam, mu, k) :
    
        rho = lam/(k*mu)

        if rho > 1 :
            print("Unstable queue")
        else :
            p0 = 0
            for i in range(k) :
                p0 += ((lam/mu)**i)/math.factorial(i)
            p0 += (pow(k,k)/math.factorial(k)) * pow(rho, k)/ (1 - rho)
            p0 = 1 / p0

            #print("p0 is : {}" .format(p0))

            p1 = p0 * ((lam/mu)**1)/math.factorial(1) 
            #print("p1 is : {}" .format(p1))

            p2 = p0 * ((lam/mu)**2)/math.factorial(2) 
            #print("p2 is : {}" .format(p2))

            #Compute expected long term length L 
            pi_w = 1 - p0 - p1 - p2
            L = (lam/mu) + (rho*pi_w)/ (1 - rho)

            #print("Long term expected length : ", L)

            #Compute long term expected response time
            W = L/lam

            #print("Long term expected response time : ", W)
            return (W - 1/mu)


    #Calculate the coeff of variance for service time distribution
    def calc_coeffvar_service(rwprop, mu_values) :

        ES = rwprop[0] / mu_values[0] + rwprop[1] / mu_values[1]
        ES2 = 2 * (rwprop[0] / (mu_values[0]**2) + rwprop[1] / (mu_values[1]**2))

        return (math.sqrt(ES2/(ES**2) - 1)), ES


    #Calculate the response time for M/G/k

    k = 2

    coeff_var, mean_serv = calc_coeffvar_service(rwprop[subtrace], mu_values)
    Wq = waiting_MMk(lam, mu, k) * (math.pow(coeff_var,2) + 1)/2
    W = Wq + 1 / mu_values[0]

    print("For subtrace_", subtrace)
    print("Waiting time in queue",Wq)
    print("Response time",W)
    
    subtrace = subtrace + 1
