#!/bin/bash

# Define the fixed parts of the script
INTRO="0:R:1:6,0:R:1:7,0:R:1:8,0:R:1:9,0:R:1:10,0:R:1:11,0:R:1:12,0:R:1:13,0:R:1:14,0.5:R:1:15,"
MID="0:r:1:0,0:b:1:0,0:s:1:0,0:v:1:0,0:h:1:0,0:r:1:0,0:b:1:0,0:s:1:0,0:v:1:0,0:h:1:0,\
0:r:1:1,0:b:1:1,0:s:1:1,0:v:1:1,0:h:1:1,0:r:1:1,0:b:1:1,0:s:1:1,0:v:1:1,0:h:1:1,\
0:r:1:2,0:b:1:2,0:s:1:2,0:v:1:2,0:h:1:2,0:r:1:2,0:b:1:2,0:s:1:2,0:v:1:2,0:h:1:2,\
0:r:1:3,0:b:1:3,0:s:1:3,0:v:1:3,0:h:1:3,0:r:1:3,0:b:1:3,0:s:1:3,0:v:1:3,0:h:1:3,\
0:r:1:4,0:b:1:4,0:s:1:4,0:v:1:4,0:h:1:4,0:r:1:4,0:b:1:4,0:s:1:4,0:v:1:4,0:h:1:4,\
0:r:1:5,0:b:1:5,0:s:1:5,0:v:1:5,0:h:1:5,0:r:1:5,0:b:1:5,0:s:1:5,0:v:1:5,0:h:1:5,\
0:r:1:6,0:b:1:6,0:s:1:6,0:v:1:6,0:h:1:6,0:r:1:6,0:b:1:6,0:s:1:6,0:v:1:6,0:h:1:6,\
0:r:1:7,0:b:1:7,0:s:1:7,0:v:1:7,0:h:1:7,0:r:1:7,0:b:1:7,0:s:1:7,0:v:1:7,0:h:1:7,\
0:r:1:8,0:b:1:8,0:s:1:8,0:v:1:8,0:h:1:8,0:r:1:8,0:b:1:8,0:s:1:8,0:v:1:8,0:h:1:8,\
0:r:1:9,0:b:1:9,0:s:1:9,0:v:1:9,0:h:1:9,0:r:1:9,0:b:1:9,0:s:1:9,0:v:1:9,0:h:1:9,"
OUTRO="0:T:1:0,0:T:1:1,0:T:1:2,0:T:1:3,0:T:1:4,0:T:1:5,0:T:1:6,0:T:1:7,0:T:1:8,0:R:1:9"

# Ensure output directories exist
mkdir -p output/a

# Loop for 10 runs
for run in {1..10}; do
    echo "Starting Run $run..."

    # Create the SCRIPT by concatenating Intro, Mid × run, and Outro
    SCRIPT="$INTRO"
    for ((i = 1; i <= run; i++)); do
        SCRIPT+="$MID"
    done
    SCRIPT+="$OUTRO"

    # Define output files
    SERVER_OUTPUT="output/a/server_run_${run}.log"
    CLIENT_OUTPUT="output/a/client_run_${run}.log"

    # Run the server and client
    /usr/bin/time -v ./build/server_mimg -q 1500 -w 1 -p FIFO 2222 >"$SERVER_OUTPUT" 2>&1 &
    sleep 1 # Allow server to initialize
    ./client 2222 -I ./images/ -L "$SCRIPT" >"$CLIENT_OUTPUT" 2>&1

    # Wait for the server process to complete
    wait

    echo "Run $run completed. Server output: $SERVER_OUTPUT, Client output: $CLIENT_OUTPUT"
done

echo "All runs completed!"