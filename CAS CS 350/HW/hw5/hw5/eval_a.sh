#!/bin/bash

# Output file where all results will be appended

# Loop to run the program 10 times
for i in {1..10}
do  
    echo "Running iteration $i..."
    # Start the server in the background and redirect its output to a file
    /usr/bin/time -v ./build/server_pol -w 2 -q 100 -p FIFO 2222 >> "result/result_a/low/FIFO_${i}_result.txt" &
    
    # Capture the process ID (PID) of the background server process
    SERVER_PID=$!

    # Wait for the server to be fully ready (small sleep to avoid race condition)
    sleep 1

    # Run the client
    ./client -a 10 -s 20 -n 1500 2222
    
    # Stop the server process after the client finishes
    kill $SERVER_PID

    echo "---------------------"
done

echo "All runs completed. Output saved in the 'result/' directory."