#!/bin/bash

# Name of your executable
program="./clock"

# Output file where all results will be appended
output_file="combined_output.txt"


# Loop to run the program 10 times
for i in {1..10}
do  
    echo "Running iteration $i..." >> $output_file
    # Save the output of each run to a file named output_<i>.txt
    $program $i 0 s >> output_$i.txt
    echo "Run $i completed." >> $output_file
    echo "---------------------" >> $output_file  # Add separator for clarity

done

echo "All runs completed. Output saved in $output_file."