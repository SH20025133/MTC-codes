#!/bin/bash

# Loop through 10 sets of files
for i in {0..1}; do
    # Form the file names based on the pattern
    file1="Partition_traces_L2/w87-L2_read_${i}.csv"
    file2="Partition_traces_L2/w87-L2_write_${i}.csv"

    # Count the number of lines in each file
    count_file1=$(wc -l < "$file1")
    count_file2=$(wc -l < "$file2")

    # Calculate the proportion
    proportion=$(echo "scale=4; $count_file1 / ($count_file1 + $count_file2)" | bc)

    # Display the results for each set of files
    echo "Set $i:"
    echo "Number of lines in $file1: $count_file1"
    echo "Number of lines in $file2: $count_file2"
    echo "Proportion: $proportion"
    echo "------------------------"
done
