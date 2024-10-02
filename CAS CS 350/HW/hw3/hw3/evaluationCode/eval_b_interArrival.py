import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# R<request ID>:<sent timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
# X<request ID>:<sent timestamp>,<request length>,<reject timestamp>

# Open the file and read the content
with open('.//result/result_b.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
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

# 1. Generate samples from the theoretical distributions
num_samples = 10000

# Normal distribution
normal_samples = np.random.normal(loc=1/4.5, scale=1, size=num_samples) # mean 1/4.5

# Exponential distribution
exponential_samples = np.random.exponential(scale=1/4.5, size=num_samples) # mean 1/4.5

# Uniform distribution
uniform_samples = np.random.uniform(low=0, high=2/4.5, size=num_samples)  # Mean 1/4.5

# 2. Plot all distributions together
plt.figure(figsize=(12, 6))

# Kernel density estimation for Normal distribution
sns.kdeplot(normal_samples, label='Normal Distribution', color='blue', linewidth=2)

# Kernel density estimation for Exponential distribution
sns.kdeplot(exponential_samples, label='Exponential Distribution', color='red', linewidth=2)

# Kernel density estimation for Uniform distribution
sns.kdeplot(uniform_samples, label='Uniform Distribution', color='green', linewidth=2)

# Kernel density estimation for experimental data
sns.kdeplot(inter_arrival_times, label='Experimental Data', color='gray', linewidth=2)

# Add labels and title
plt.title('Comparison of inter-arrival Distributions of -d 2')
plt.xlabel('inter-arrival')
plt.ylabel('Density')
plt.legend()

# Show the plot
plt.show()
