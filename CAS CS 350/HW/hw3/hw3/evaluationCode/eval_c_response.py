
import numpy as np

# R<request ID>:<sent timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>


# Average Response time = Average of (Completion - send (by client) timestamp)

#R0:3770578.606080,0.033434,3770578.606203,3770578.606240,3770578.639700

# Open the file and read the content
with open('.//result/result_c/d0/-a10_result.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()

# Initialize a array to save response time
response_time = []

for line in lines:
    parts = line.strip()
    
    # Grab only Response output
    if line.startswith("R"):
        parts = line.split(',')
        completion_timestamp = float(parts[4]) 
        send_timestamp = float(parts[0].split(':')[1])

        response_time.append(completion_timestamp - send_timestamp)

average_response_time = sum(response_time) / len(response_time)
print(len(response_time))
print(f"Average Response time : {average_response_time}\n")
