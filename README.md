# MTC-codes
Contains data and codes for different queueing models used on cloudphysics traces
Steps

We take the entire trace and based on src values (and the ways discussed on slide)
divide it into L1 reads, L1 writes, L2 reads, L2 writes.

Thus, at the end of initial_filter.py you would have 4 csv files

Next for cp detection, we use a single set of values to detect a common set of cps that would partition both L1 & L2
(unlike before where we were doing the cp detection seperately for L1 and L2)

For this, we use the "G1" & "G2" columns from the trace and the follow the ideas discussed. on the slides 

Execute the extract_G.py file to extract all G's and then go about the normal way
- csv_grouprequests.py  //To give arrival rates/min
- Beast.py             //Detect cps in minutes

Now execute csv_preprocessing.py to extract all Q values from the 4 files (something similar to extracting I from L1 and L2 previously). You will 4 files with "_Q.csv". Time to do CDF partition on these 4 files to have subtraces

With these you are ready to do IAT fits for the 2 classes across 2 devices.

A bit of a backtrack (to verify if the read/write ratio is consistent within a subtrace.) 

To do this (say for L1) :

-You shall need to count the number of reads and writes simultaneously in each minute in say two dataframes (execute plot_readratio.ipynb)
-calculate the ratio
-and plot if necessary
