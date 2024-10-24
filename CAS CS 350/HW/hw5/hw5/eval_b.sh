#!/bin/bash

# Set up result directory
result_dir="result/result_b"
mkdir -p "$result_dir"

# Run experiments for both FIFO and SJN policies
for policy in FIFO SJN
do
    echo "Starting experiments for $policy policy..."
    
    # Run 10 times, increasing arrival rate from 22 to 40 by 2 each time
    for arr_rate in $(seq 22 2 40)
    do
        echo "Running experiment with arrival rate $arr_rate..."
        
        output_file="${result_dir}/${policy}_${arr_rate}_result.txt"
        
        # Start the server
        /usr/bin/time -v ./build/server_pol -w 2 -q 100 -p $policy 2222 > "$output_file" 2>&1 &
        server_pid=$!
        
        # Wait briefly for the server to be ready
        sleep 1
        
        # Run the client
        ./client -a $arr_rate -s 20 -n 1500 2222
        
        # Stop the server process
        kill $server_pid
        wait $server_pid 2>/dev/null
        
        echo "Experiment with arrival rate $arr_rate completed. Results saved to $output_file"
    done
    
    echo "All experiments for $policy policy completed."
done

echo "All experiments have been completed. Results are saved in the $result_dir directory."


