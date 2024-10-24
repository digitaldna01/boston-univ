import os
import re
import numpy as np
import matplotlib.pyplot as plt

def parse_file(filepath):
    utilization = 0
    total_response_time = 0
    request_count = 0
    first_receipt = None
    last_complete = None
    total_service_time = 0

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('T'):
                parts = line.split(':')[1].split(',')
                send_timestamp = float(parts[0])
                request_length = float(parts[1])
                receipt = float(parts[2])
                start = float(parts[3])
                complete = float(parts[4])

                total_service_time += request_length
                total_response_time += complete - send_timestamp
                request_count += 1

                if first_receipt is None:
                    first_receipt = receipt
                last_complete = complete

    total_time = last_complete - first_receipt
    utilization = total_service_time / (total_time * 2)  # 2 workers
    avg_response_time = total_response_time / request_count

    return utilization, avg_response_time

def process_results(directory, policy):
    results = []
    pattern = rf"{policy}_\d+_result\.txt"
    
    for filename in sorted(os.listdir(directory)):
        if re.match(pattern, filename):
            filepath = os.path.join(directory, filename)
            util, resp_time = parse_file(filepath)
            results.append((util, resp_time))
    
    return results

# Set directory
directory = "result/result_b"

# Process results for FIFO and SJN
fifo_results = process_results(directory, "FIFO")
sjn_results = process_results(directory, "SJN")

# Draw graph
fifo_utils, fifo_resp_times = zip(*fifo_results)
sjn_utils, sjn_resp_times = zip(*sjn_results)

plt.figure(figsize=(10, 6))
plt.plot(fifo_utils, fifo_resp_times, 'bo-', label='FIFO')
plt.plot(sjn_utils, sjn_resp_times, 'ro-', label='SJN')
plt.xlabel('Server Utilization')
plt.ylabel('Average Response Time (seconds)')
plt.title('Response Time vs Server Utilization')
plt.legend()
plt.grid(True)
plt.savefig('response_time_vs_utilization.png')
plt.close()

# Print results
print("FIFO Results:")
for util, resp_time in fifo_results:
    print(f"Utilization: {util:.2f}, Response Time: {resp_time:.4f}")

print("\nSJN Results:")
for util, resp_time in sjn_results:
    print(f"Utilization: {util:.2f}, Response Time: {resp_time:.4f}")

# Genenralize the result
fifo_avg_resp_time = np.mean([rt for _, rt in fifo_results])
sjn_avg_resp_time = np.mean([rt for _, rt in sjn_results])
difference = fifo_avg_resp_time - sjn_avg_resp_time
percentage = (difference / fifo_avg_resp_time) * 100

print(f"\nOverall, SJN is {difference:.4f} seconds faster on average.")
print(f"This represents a {percentage:.2f}% improvement over FIFO.")
