import matplotlib.pyplot as plt
import numpy as np

# the line structure : R<ID>:<send timestamp>,<length>,<receipt timestamp>,<completion timestamp>
# R0:3642924.618835,0.050151,3642924.618935,3642924.669121

# Open the file and read the content
with open('.//result/eval1_raw_result.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()

# define the data array set
data = []

#### Preprocessing the data
for line in lines:
    line = line.strip()
    
    if line.startswith("R"):
        parts = line.split(',')
        lengths = float(parts[1])
        
        # Add append the data set with each lengths of the request
        data.append(lengths)

#### Create the distribution histogram

# Define bin edges with 0.005 increments
bin_edges = np.arange(0, max(data) + 0.005, 0.005)

# Calculate the histogram (counts and bin edges)
counts, _ = np.histogram(data, bins=bin_edges)

# Normalize the counts by dividing by the total number of requests
normalized_counts = counts / len(data)  # len(data) should be 1000 as per your example

# Plot the distribution
plt.bar(bin_edges[:-1], normalized_counts, width=0.005, align='edge', edgecolor='black', alpha=0.7)

# Add labels and title
plt.title('Normalized Distribution of Request Lengths')
plt.xlabel('Request Length (seconds)')
plt.ylabel('Normalized Frequency')

plt.show()

# print(len(data))
# print(data[0])

