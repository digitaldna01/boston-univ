import matplotlib.pyplot as plt
import numpy as np

# the line structure : R<ID>:<send timestamp>,<length>,<receipt timestamp>,<completion timestamp>
# R0:3642924.618835,0.050151,3642924.618935,3642924.669121

# Open the file and read the content
with open('.//result/eval1_raw_result.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()

# Define an array to store the send timestamps
timestamps = []

# Preprocess the data to extract send timestamps
for line in lines:
    line = line.strip()
    
    if line.startswith("R"):
        parts = line.split(',')
        send_timestamp = float(parts[0].split(':')[1])
        
        # Append each send timestamp
        timestamps.append(send_timestamp)
        
# Calculate the inter-arrival times
inter_arrival_times = []
for i in range(1, len(timestamps)):
    inter_arrival_time = timestamps[i] - timestamps[i - 1]
    inter_arrival_times.append(inter_arrival_time)

# Define bin edges with 0.005 increments
bin_edges = np.arange(0, max(inter_arrival_times) + 0.005, 0.005)

# Calculate the histogram (counts and bin edges)
counts, _ = np.histogram(inter_arrival_times, bins=bin_edges)

# Normalize the counts by dividing by 999 (total number of inter-arrival times)
normalized_counts = counts / 999

# Plot the distribution
plt.bar(bin_edges[:-1], normalized_counts, width=0.005, align='edge', edgecolor='black', alpha=0.7)

# Add labels and title
plt.title('Normalized Distribution of Inter-Arrival Times')
plt.xlabel('Inter-Arrival Time (seconds)')
plt.ylabel('Normalized Frequency')

# Show the plot
plt.show()