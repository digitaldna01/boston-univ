import re
import matplotlib.pyplot as plt

# the line structure : T<id> R<ID>:<send timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>

# Function to extract response times from a log file
def extract_response_times(log_file):
    response_times = []
    
    with open(log_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Match the relevant log pattern for requests
            if line.startswith("T"):
                parts = line.split(',')
                completion_timestamp = float(parts[4]) 
                send_timestamp = float(parts[0].split(':')[1])
                
                response_time = completion_timestamp - send_timestamp
                response_times.append(response_time)
    
    # Calculate average response time
    if response_times:
        return sum(response_times) / len(response_times)
    else:
        return 0

# List of log files corresponding to different thread counts
log_files = {
    2: './/result/eval_b.txt',
    4: './/result/eval_c_4.txt',
    6: './/result/eval_c_6.txt',
    8: './/result/eval_c_8.txt'
}

# Store the average response times for each thread count
thread_counts = []
avg_response_times = []

for threads, log_file in log_files.items():
    avg_time = extract_response_times(log_file)
    thread_counts.append(threads)
    avg_response_times.append(avg_time)

# Plot the results
plt.plot(thread_counts, avg_response_times, marker='o')
plt.xlabel('Number of Threads')
plt.ylabel('Average Response Time (seconds)')
plt.title('Average Response Time vs. Number of Threads')
plt.grid(True)
plt.show()

print(thread_counts)
print(avg_response_times)
