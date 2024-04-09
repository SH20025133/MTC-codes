"""
This code will have two parts inside G1/G/2 where

-G1  is a H2 distribution of arrivals as rexp(r) + wexp(w)
-G is a H2 distribution of service as rexp(r) + wexp(w)


The only line you'll change for read-only and write-only is #266 as mu_values[0] for reads or mu_values[1] for writes

We have used Matrix analytics method to determine RT of H2/H2/2 queues. So, the results are approximate (infact excellent approximates) .
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

    
    except IndexError : #Cases where the lam and mu parametres could not be determined and were NULL
        
        lam_values = [100, 100]
        mu_values = [100, 100]
        

    print("lam1, lam2, mu1, mu2, p : ",lam_values, mu_values, rwprop[subtrace])
    
    lam1 = lam_values[0]
    lam2 = lam_values[1]
    p = rwprop[subtrace][0]
    
    mu1 = mu_values[0]
    mu2 = mu_values[1]
    q = rwprop[subtrace][0]
    
    b1 = 2*mu1*(1-q)
    b2 = 2*mu2*(1-q)
    b3 = 2*mu1*q
    b4 = 2*mu2*q
    f1 = lam1*(1-p)
    f2 = lam2*(1-p)
    f3 = lam1*p
    f4 = lam2*p
    
     #Initializing forward, backward and initial arrays
    L_0 = np.transpose(np.array([[-(lam1), 0],
                   [0, -(lam2)]]))
   # print(L_0)
    #F_0 = np.array([[lam1*p*q, lam1*(1-p)*q, lam1*p*(1-q), lam1*(1-p)*(1-q)],
    #               [lam2*(1-p)*(1-q), lam2*p*(1-q), lam2*p*q, lam2*(1-p)*q]])

    F_0 = np.array([[lam1*p*q, lam1*(1-p)*q, lam1*p*(1-q), lam1*(1-p)*(1-q)],
                  #[lam2*p*q, lam2*(p)*(1-q), lam2*(1-p)*(q), lam2*(1-p)*(1-q)],
                   [lam2*(p)*(q), lam2*(1-p)*(q), lam2*(p)*(1-q), lam2*(1-p)*(1-q)]])
   # print(F_0)
    B_0 = np.array([[mu1, 0],
                   [mu1, 0],
                   [0, mu2],
                   [0, mu2]])
   # print(B_0)
    L = np.array([[-(lam1 + 2*mu1), 0, 0, 0],
                 [0, -(lam2 + 2*mu1), 0, 0],
                 [0, 0, -(lam1 + 2*mu2), 0],
                 [0, 0, 0, -(lam2 + 2*mu2)]])
    L_1 = np.array([[-(lam1 + mu1), 0, 0, 0],
                 [0, -(lam2 + mu1), 0, 0],
                 [0, 0, -(lam1 + mu2), 0],
                 [0, 0, 0, -(lam2 + mu2)]])
   # print(L)
   # print(L_1)
    F = np.array([[f3, f1, 0, 0],
                 [f4, f2, 0, 0],
                 [0, 0, f3, f1],
                 [0, 0, f4, f2]])
    #print(F)
    B = np.array([[b3, 0, b1, 0],
                 [0, b3, 0, b1],
                 [b4, 0, b2, 0],
                 [0, b4, 0, b2]])
    B1 = np.array([[mu1*q, 0, mu1*(1-q), 0],
                 [0, mu1*q, 0, mu1*(1-q)],
                 [mu2*q, 0, mu2*(1-q), 0],
                 [0, mu2*q, 0, mu2*(1-q)]])
    #print(B)
    #print(B1)
    R_0 = np.zeros((4, 4))
    #print(R_0)
    
    R_prev = R_0
    n = 0
    flag = 0

    while flag == 0 :
        diff = []
        if n > 0:
            R_prev = R

        R_2 = np.matmul(R_prev,R_prev)
        R_mid = -(np.matmul(R_2,B) + F)
        #print(R_mid)
        R = np.matmul(R_mid, np.linalg.inv(L))

        for (i,j) in zip(R_prev, R) :
            for (k,l) in zip(i,j) :
                diff.append(abs(k-l))

        max = np.max(diff)
        #print("Max is", max)
        if (max < 10**-7) :

            flag =1
            break
        n += 1
   # print(R,n)
    
    #Computing steady state distribution for state 0 and 1

    #Creating (I - R)^-1 = psi
    I = np.eye(4)
    psi_full = np.linalg.inv(I - R)
    psi = np.matmul(psi_full,np.ones((4,1), dtype=int))
    psi = np.vstack([np.ones((6,1), dtype=int), psi])
    #print("Psi :",psi)

    #Creating L + RB
    RB = np.matmul(R, B)
    LRB = np.add(L, RB)
   # print(LRB)

    #Creating stacked version of [0  F  L+RB]T = phi
    phi_2 = np.vstack([np.zeros((2, 4)), F, LRB])


    #Creating stacked version of [F_0 L_1 B]
    phi_1 = np.vstack([F_0, L_1, B])

    phi = np.hstack([phi_1, phi_2])
    #print("Phi :",phi)

    #Solving for pi_0 and pi_1
    A = np.array([0, -(lam2), 0, 0, mu2, mu2, 0, 0, 0, 0])
    A = A[..., None] 

    A = np.hstack([psi,A, phi])
    b = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
   # print(A,b)
    """
    steady_pi = np.linalg.solve(np.transpose(A), b)
    print(steady_pi)
    """
    steady_pi = np.matmul(b, np.linalg.inv(A)) 
    #print(steady_pi)
    #print(b.shape)
    
    lam_avg = (p/(lam1) + (1-p)/(lam2))
    
    
    pi_1 = [steady_pi[2], steady_pi[3], steady_pi[4], steady_pi[5]]
   # print("pi_1 : ", pi_1)

    pi_2 = [steady_pi[6], steady_pi[7], steady_pi[8], steady_pi[9]]
   # print("pi_2 : ", pi_2)

    squareI_R = np.matmul((I - R), (I - R)) 
    W_num_1 = np.matmul(np.linalg.inv(squareI_R), np.ones((4,1), dtype=int))
    W_num_1 = np.matmul(R, W_num_1)
    #print(W_num_1)

    W_num_2 = 2*np.matmul(np.linalg.inv(I - R), np.ones((4,1), dtype=int))
    #print(W_num_2)
    W_num = np.dot(pi_2, W_num_1 + W_num_2)

    W_num = W_num + np.matmul(pi_1, np.ones((4,1), dtype=int))
    W_whole = W_num * lam_avg
    
    #calculate wait time in queue Wq
    
    Wq = W_whole - ((q/mu1) + ((1-q)/mu2))
    
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
    
