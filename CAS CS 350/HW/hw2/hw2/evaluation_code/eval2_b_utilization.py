import numpy as np

# Utilization =  = Time Resource is busy / Total Available Time

# Time Resource is busy = sum (completetion - start for each request )
# Total Available time = R999 completion - R0 start 

# the line structure : R<ID>:<send timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
#R0:3770578.606080,0.033434,3770578.606203,3770578.606240,3770578.639700

# Open the file and read the content
with open('.//result/eval2_a15_result.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()
    
# Initialize a total seconds to hold the sum
total_busy_resouces_sec = 0.0

for line in lines:
    parts = line.strip()
    
    # Grab only Response output
    if line.startswith("R"):
        parts = line.split(',')
        busy_resource_timestamp = float(parts[4]) - float(parts[3])
        
        total_busy_resouces_sec += busy_resource_timestamp

print(f"total busy resouces sec : {total_busy_resouces_sec}\n")

index = 0
start_receipt_timestamp = 0
end_completion_timestamp = 0
total_available_time = 0

for line in lines:
    parts = line.strip()
    
    # Grab only Response output
    if line.startswith("R"):
        parts = line.split(',')
        if index == 0:
            start_receipt_timestamp =  float(parts[3])
        elif index == 999:
            end_completion_timestamp = float(parts[4])
        index += 1
        
total_available_time = end_completion_timestamp - start_receipt_timestamp
print(f"total available time: {total_available_time}\n")

utilization = total_busy_resouces_sec / total_available_time
print(f"Utilization : {utilization}\n")
    
    
