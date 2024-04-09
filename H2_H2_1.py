"""
This code will have two parts inside G1/G/1 where

-G1  is a H2 distribution of arrivals as rexp(r) + wexp(w)
-G is a H2 distribution of service as rexp(r) + wexp(w)


The only line you'll change for read-only and write-only is #142 as mu_values[0] for reads or mu_values[1] for writes

We have used the closed form solution for response time and waiting time as derived in Tarasov's paper
"""

import pandas as pd
import math
from sympy import symbols, solve, re
import numpy as np

inp_fn = "allfitw64-SH-iodepth64-clsize64-mtc-L2"
df_iat = pd.read_csv(inp_fn+".csv")
df_iat1 = df_iat
df_st = pd.read_csv(inp_fn+"_ST.csv")
df_st1 = df_st
#f_out = open(inp_fn+".csv","w")

df_exp_iat = df_iat[df_iat.DistName == "exponential"]
df_exp_st = df_st[df_st.DistName == "exponential"]




rwprop = [(.9415, 1-.9415), (.0092, 1-.0092), (.0468, 1-.0468), (.0166, 1-.0166), (.0958, 1-.0958), (.0378, 1-.0378), (.0714, 1-.0714), (.0051, 1-.0051), (.0432, 1-.0432)]
"""

rwprop = [(0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0), (0, 1-0)]
"""

#print("Length of rwprop", len(rwprop))
subtrace = 0
r_line = ""


while subtrace <= 8 :
    
    lam_values = []
    mu_values = []
    
    try :
    
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

    
    except IndexError :
        
        lam_values = [100, 100]
        mu_values = [100, 100]
        

    print("lam1, lam2, mu1, mu2, p : ",lam_values, mu_values, rwprop[subtrace])
    
    lam_1 = lam_values[0]
    lam_2 = lam_values[1]
    p = rwprop[subtrace][0]
    
    mu_1 = mu_values[0]
    mu_2 = mu_values[1]
    q = rwprop[subtrace][0]
    
    a_0 = (lam_1*lam_2)
    a_1 = p*lam_1 + (1-p)*lam_2
    b_0 = (mu_1*mu_2)
    b_1 = q*mu_1 + (1-q)*mu_2

    c_0 = a_0*b_1 - a_1*b_0 - a_0*(mu_1+mu_2) + b_0*(lam_1 + lam_2)
    c_1 = -a_1*b_1 -a_0 - b_0  + (lam_1 + lam_2)*(mu_1 + mu_2)
    c_2 = lam_1 + lam_2 - mu_1 - mu_2
    
    x = symbols('x')
    expr = x**3-c_2*x**2-c_1*x-c_0


    sol = solve(expr)
    print(sol)
    
    #calculate wait time in queue Wq
    
    Wq = (-1/re(sol[0])) + (-1/re(sol[1])) - (1/mu_1) - (1/mu_2) 
    
    """

    #Calculate E[S]

    def calcS(mu_values, rwprop) :
        ES = rwprop[0] / mu_values[0] + rwprop[1] / mu_values[1]
        
        #print("*",ES)
        return ES

    #print("Mean service time in us", calcS(mu_values, rwprop[subtrace]))

    #Calculate E[S^2]

    def calcS2(mu_values, rwprop) :
        ES2 = 2 * (rwprop[0] / (mu_values[0]**2) + rwprop[1] / (mu_values[1]**2))
        
        #print("**",ES2)
        return ES2
        
    """

    print("For subtrace_", subtrace)
    
    #rho = lam * calcS(mu_values, rwprop[subtrace])
    #print("Load factor", rho)
    
    """
    rho2 = lam * (mu_values[0] + mu_values[1])
    print("Actual Load factor", rho2)
    """


    #calculate wait time in queue Wq
   # calc_variance = calcS2(mu_values, rwprop[subtrace]) - calcS(mu_values, rwprop[subtrace])**2

    
    W = Wq + 1 / mu_values[1]
    #Lq = lam * Wq
    #Lq = ((lam**2)*calc_variance + rho**2) / 2 * (1 - rho)

    
    print("Waiting time in queue",Wq)
    print("Response time",W)
    
    subtrace = subtrace + 1
    
