import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# R<ID>:<send timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
# X<ID>:<send timestamp>,<request length>,<reject timestamp>
# Open the file and read the content
with open('.//result/eval_d_2.txt', 'r') as file:  # Adjust to your file path
    lines = file.readlines()
    
# Variables to store data
total_requests = 0
rejected_requests = 0
rejection_timestamps = []

# Process each line from the server output
for line in lines:
    line = line.strip()
    
    if line.startswith("R"):  # "R" indicates a regular processed request
        total_requests += 1
    
    elif line.startswith("X"):  # "X" indicates a rejected request
        total_requests += 1
        rejected_requests += 1
        parts = line.split(',')
        rejection_timestamp = float(parts[2])  # Extract the reject timestamp
        rejection_timestamps.append(rejection_timestamp)

# Calculate the rejection ratio
rejection_ratio = rejected_requests / total_requests
print(f"Rejection Ratio: {rejection_ratio:.4f}")
print("Rejection  number:", rejected_requests)
# Calculate inter-rejection times
inter_rejection_times = np.diff(rejection_timestamps)

# Plotting the inter-rejection time distribution
plt.figure(figsize=(10, 6))

# Use Seaborn's KDE plot to visualize the distribution
sns.histplot(inter_rejection_times, kde=True, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Inter-Rejection Time Distribution')
plt.xlabel('Time between rejections')
plt.ylabel('Frequency')

plt.show()
