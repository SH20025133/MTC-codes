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


inp_fn1 = "allfitw64-SH-iodepth64-clsize64-mtc-L1"
inp_fn2 = "allfitw64-SH-iodepth64-clsize64-mtc-L2"
df_L1 = pd.read_csv(inp_fn1+"_ST.csv")

df_L2 = pd.read_csv(inp_fn2+"_ST.csv")
#f_out = open(inp_fn+".csv","w")

#df_exp_iat = df_iat[df_iat.DistName == "exponential"]
df_exp_stL1 = df_L1[df_L1.DistName == "exponential"]
df_exp_stL2 = df_L2[df_L2.DistName == "exponential"]

#df_hyperexp_subtrace_stL1_write = df_exp_stL1[df_exp_stL1.fname.str.contains("_write_")]
#df_hyperexp_subtrace_stL2_write = df_exp_stL2[df_exp_stL2.fname.str.contains("_write_")]

#print(df_hyperexp_subtrace_stL1_write)
#print(df_hyperexp_subtrace_stL2_write)

subtrace = 0
r_line = ""

rwpropL1 = [0.0026, 0.0297, 0.0297, 0.9186, 0.9755, 0.0646, 0.0505, 0.0456, 0.098]

rwpropL2 = [0.9415, 0.0092, 0.0468, 0.0166, 0.0958, 0.0378, 0.0714, 0.0051, 0.0432]

while subtrace <= 8 :
    
    #lam1, lam2, lam3, lam4
    lam_values = []
    #p1, p2
    p_values = []
    
    df_hyperexp_subtrace_stL1_read = df_exp_stL1[df_exp_stL1.fname.str.contains("_read_ST_"+str(subtrace))]
    df_hyperexp_subtrace_stL1_write = df_exp_stL1[df_exp_stL1.fname.str.contains("_write_ST_"+str(subtrace))]
    df_hyperexp_subtrace_stL2_read = df_exp_stL2[df_exp_stL2.fname.str.contains("_read_ST_"+str(subtrace))]
    df_hyperexp_subtrace_stL2_write = df_exp_stL2[df_exp_stL2.fname.str.contains("_write_ST_"+str(subtrace))]
    
    #print(df_hyperexp_subtrace_stL1_write)
    #print(df_hyperexp_subtrace_stL2_write)
    
    lam_values.append(1/df_hyperexp_subtrace_stL1_read.Params_1.values[0])
    lam_values.append(1/df_hyperexp_subtrace_stL1_write.Params_1.values[0])
    lam_values.append(1/df_hyperexp_subtrace_stL2_read.Params_1.values[0])
    lam_values.append(1/df_hyperexp_subtrace_stL2_write.Params_1.values[0])
    
    print(lam_values)
    
    p_values.append(rwpropL1[subtrace])
    p_values.append(rwpropL2[subtrace])
    
    print(p_values)
    
    maxvalue_1 = (1 - p_values[0])/lam_values[1] + p_values[0]/lam_values[0] + (lam_values[0]+lam_values[3]-                         lam_values[0]*p_values[0] + lam_values[1]*p_values[0])/((lam_values[0]+lam_values[3])*(lam_values[1]+lam_values[3])) + (1-       p_values[1])/lam_values[3] + p_values[1]*lam_values[1]/(lam_values[2]*(lam_values[1]+ lam_values[2]))
    
    maxvalue_2 = p_values[1] * (1 / (lam_values[1] + lam_values[3]) + p_values[0] * (
    (1 / (lam_values[1] + lam_values[2])) - (1 / (lam_values[0] + lam_values[2])) + (1 / (lam_values[0] + lam_values[3])) - (1 /     (lam_values[1] + lam_values[3]))))
                              
    maxvalue_total = maxvalue_1 + maxvalue_2
    
    print("For subtrace_", subtrace)  
    print("Max of L1 and L2 writes(RT)",maxvalue_total)
    
    
    subtrace = subtrace + 1
    
