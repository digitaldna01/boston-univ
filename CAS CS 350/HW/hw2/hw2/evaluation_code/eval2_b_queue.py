import numpy as np

# the line structure : R<ID>:<send timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
#R0:3770578.606080,0.033434,3770578.606203,3770578.606240,3770578.639700

# Open the file and read the content
with open('.//result/eval2_a15_result.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()

completion_timestamp = []

#### Preprocessing the data
for line in lines:
    line = line.strip()
    
    if line.startswith("R"):
        parts = line.split(',')
        lengths = float(parts[-1])
        
        # Add append the data set with each lengths of the request
        completion_timestamp.append(lengths)
        
# Calculate the inter-arrival times
inter_completion_timestamp = []
inter_timestamp = 0
for i in range(1, len(completion_timestamp)):
    inter_timestamp = completion_timestamp[i] - completion_timestamp[i - 1]
    inter_completion_timestamp.append(inter_timestamp)

total_completion_timestap = sum(inter_completion_timestamp)

# print(len(inter_completion_timestamp))

index  = 0
average_queue = 0
for line in lines:
    line = line.strip()
    
    if index < 999 and  line.startswith("Q"):
        r_count = line.count('R')
        queue_value = r_count * (inter_completion_timestamp[index]/total_completion_timestap)
        average_queue += queue_value
        index += 1

print(average_queue)
