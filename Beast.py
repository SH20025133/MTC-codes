import Rbeast as rb
import pandas as pd
import numpy as np

df = pd.read_csv('CPD/w53-SH__min_without.csv')
ser = df.iloc[:,0]
ser1 = ser[:100000]
len(ser)
#interval2 = pd.Interval(10, 30)
#interval1 = pd.Interval(0, 1)

my_bkps = rb.beast(ser,season='None', tcp_minmax = [0,25])
print(id(my_bkps))
#print(my_bkps.trend.cp)
#print(my_bkps.trend.cpPr)
#print(my_bkps.ocp_max)

#Converting arrays to lists

cp_list = sorted(my_bkps.trend.cp.tolist())
cp_prob = sorted(my_bkps.trend.cpPr.tolist())
cp_list_updated = []
cp_prob_updated = []

#Filtering cps
i = 0
for i in range(len(cp_prob) - 1) :
    if cp_prob[i] < 0.5 or (cp_list[i+1] - cp_list[i] <= 10) or (np.isnan(cp_prob[i])):
        i += 1
        continue
    else :
        cp_list_updated.append(cp_list[i])
        cp_prob_updated.append(cp_prob[i])
        i += 1
        
print(cp_list_updated)
print(np.round(cp_prob_updated,4))
print(len(cp_list_updated))

print(cp_list)
print(np.round(cp_prob,2))
print(len(cp_list))
