import pandas as pd
import math

"""
Mathematical expression for max of two H2's
First H2 = p1exp(lam1) + (1-p1)exp(lam2)
First H2 = p2exp(lam3) + (1-p2)exp(lam4)


 lam1 + lam4 - lam1 p1 + lam2 p1)/((lam1 + lam4) (lam2 + lam4)) + (
  1 - p2)/lam4 + (lam2 p2)/(
  lam3 (lam2 + lam3)) + (1/(
 	lam2 + lam4) + (-(1/(lam1 + lam3)) + 1/(lam2 + lam3) + 1/(
    	lam1 + lam4) - 1/(lam2 + lam4)) p1) p2
        
"""
"""

inp_fn1 = "allfitw64-SH-iodepth16-clsize64-mtc-L1"
inp_fn2 = "allfitw64-SH-iodepth16-clsize64-mtc-L2"
df_L1 = pd.read_csv(inp_fn1+"_ST_theory.csv")

df_L2 = pd.read_csv(inp_fn2+"_ST_theory.csv")
#f_out = open(inp_fn+".csv","w")

#df_exp_iat = df_iat[df_iat.DistName == "exponential"]
df_exp_stL1 = df_L1[df_L1.DistName == "hyperexp"]
df_exp_stL2 = df_L2[df_L2.DistName == "hyperexp"]

#df_hyperexp_subtrace_stL1_write = df_exp_stL1[df_exp_stL1.fname.str.contains("_write_")]
#df_hyperexp_subtrace_stL2_write = df_exp_stL2[df_exp_stL2.fname.str.contains("_write_")]

#print(df_hyperexp_subtrace_stL1_write)
#print(df_hyperexp_subtrace_stL2_write)

subtrace = 0
r_line = ""


while subtrace <= 6 :
    
    #lam1, lam2, lam3, lam4
    lam_values = []
    #p1, p2
    p_values = []
    
    df_hyperexp_subtrace_stL1_write = df_exp_stL1[df_exp_stL1.fname.str.contains("_write_ST_"+str(subtrace))]
    df_hyperexp_subtrace_stL2_write = df_exp_stL2[df_exp_stL2.fname.str.contains("_write_ST_"+str(subtrace))]
    
    #print(df_hyperexp_subtrace_stL1_write)
    #print(df_hyperexp_subtrace_stL2_write)
    
    lam_values.append(df_hyperexp_subtrace_stL1_write.Params_1.values[0])
    lam_values.append(df_hyperexp_subtrace_stL1_write.Params_2.values[0])
    lam_values.append(df_hyperexp_subtrace_stL2_write.Params_1.values[0])
    lam_values.append(df_hyperexp_subtrace_stL2_write.Params_2.values[0])
"""
inp_fn1 = pd.read_csv("results_RTdist_w64L1.csv")
inp_fn2 = pd.read_csv("results_RTdist_w64L2.csv")

subtrace = 0
r_line = ""


while subtrace <= 8 :
    
    #lam1, lam2, lam3, lam4
    lam_values = []
    #p1, p2
    p_values = []

    lam_values.append(inp_fn1.loc[subtrace, "mu1"])
    lam_values.append(inp_fn1.loc[subtrace, "mu2"])
    lam_values.append(inp_fn2.loc[subtrace, "mu1"])
    lam_values.append(inp_fn2.loc[subtrace, "mu2"])
    
    
    
    p_values.append(inp_fn1.loc[subtrace, "q"])
    p_values.append(inp_fn2.loc[subtrace, "q"])
    
    maxvalue_1 = (1 - p_values[0])/lam_values[1] + p_values[0]/lam_values[0] + (lam_values[0]+lam_values[3]-                         lam_values[0]*p_values[0] + lam_values[1]*p_values[0])/((lam_values[0]+lam_values[3])*(lam_values[1]+lam_values[3])) + (1-       p_values[1])/lam_values[3] + p_values[1]*lam_values[1]/(lam_values[2]*(lam_values[1]+ lam_values[2]))
    
    maxvalue_2 = p_values[1] * (1 / (lam_values[1] + lam_values[3]) + p_values[0] * (
    (1 / (lam_values[1] + lam_values[2])) - (1 / (lam_values[0] + lam_values[2])) + (1 / (lam_values[0] + lam_values[3])) - (1 /     (lam_values[1] + lam_values[3]))))
                              
    maxvalue_total = maxvalue_1 + maxvalue_2
    
    print("For subtrace_", subtrace)  
    print(lam_values)
    print("Max of L1 and L2 writes(RT)",maxvalue_total)
    
    
    subtrace = subtrace + 1
    
