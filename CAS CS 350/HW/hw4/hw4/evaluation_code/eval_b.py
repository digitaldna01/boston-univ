# Utilization =  = Time Resource is busy / Total Available Time

# Time Resource is busy = sum (completetion - start for each request )
# Total Available time = R1499 completion - R0 start for each thread


# the line structure : T<id> R<ID>:<send timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
#R0:3770578.606080,0.033434,3770578.606203,3770578.606240,3770578.639700

# Open the file and read the content
with open('.//result/eval_b.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()
    
# Initialize a total seconds to hold the sum
index_0 = 0
index_1 = 0

start_receipt_timestamp_0 = 0.0
start_receipt_timestamp_1 = 0.0

end_completion_timestamp_0 = 0.0
end_completion_timestamp_1 = 0.0

total_busy_resource_sec_0 = 0.0
total_busy_resource_sec_1 = 0.0

for line in lines:
    parts = line.strip()
    
    # Grab only Response output
    if line.startswith("T0"):
        parts0 = line.split(',')
        if (index_0 == 0):
            start_receipt_timestamp_0 = float(parts0[3])
        
        busy_resource_timestamp_0 = float(parts0[4]) - float(parts0[3]) # completion timestam - start timestamp
        end_completion_timestamp_0 = float(parts0[4])
        total_busy_resource_sec_0 += busy_resource_timestamp_0
        index_0 += 1
        
    if line.startswith("T1"):
        parts1 = line.split(',')
        if (index_1 == 0):
            start_receipt_timestamp_1 = float(parts1[3])
        busy_resource_timestamp_1 = float(parts1[4]) - float(parts1[3]) # completion timestam - start timestamp
        end_completion_timestamp_1 = float(parts1[4])
        total_busy_resource_sec_1 += busy_resource_timestamp_1
        index_1 += 1


print(f"total Thread 0 busy resouces sec : {total_busy_resource_sec_0}")
print(f"total Thread 1 busy resouces sec : {total_busy_resource_sec_1}\n")

        
total_available_time_0 = end_completion_timestamp_0 - start_receipt_timestamp_0
total_available_time_1 = end_completion_timestamp_1 - start_receipt_timestamp_1
print(f"Thread 0 total available time: {total_available_time_0}")
print(f"Thread 1 total available time: {total_available_time_1}\n")

utilization_0 = total_busy_resource_sec_0 / total_available_time_0
utilization_1 = total_busy_resource_sec_1 / total_available_time_1
print(f"Thread 0 Utilization : {utilization_0}")
print(f"Thread 1 Utilization : {utilization_1}\n")    

print(f"Thread 0 Number of Request : {index_0}")
print(f"Thread 1 Number of Request : {index_1}\n")

