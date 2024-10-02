import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# R<request ID>:<sent timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
# X<request ID>:<sent timestamp>,<request length>,<reject timestamp>

# Open the file and read the content
with open('.//result/result_a.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
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

print(data)
# 1. Generate samples from the theoretical distributions
num_samples = 10000

# Normal distribution
normal_samples = np.random.normal(loc=1/5, scale=1, size=num_samples) # mean 1/10

# Exponential distribution
exponential_samples = np.random.exponential(scale=1/5, size=num_samples) # mean 1/10

# Uniform distribution
uniform_samples = np.random.uniform(low=0, high=2/5, size=num_samples)  # Mean 1/10

# 2. Plot all distributions together
plt.figure(figsize=(12, 6))

# Kernel density estimation for Normal distribution
sns.kdeplot(normal_samples, label='Normal Distribution', color='blue', linewidth=2)

# Kernel density estimation for Exponential distribution
sns.kdeplot(exponential_samples, label='Exponential Distribution', color='red', linewidth=2)

# # Plotting the histogram for experimental data
# sns.histplot(data, bins=30, color='gray', kde=False, label='Experimental Data', stat='density', alpha=0.5)

# Kernel density estimation for Uniform distribution
sns.kdeplot(uniform_samples, label='Uniform Distribution', color='green', linewidth=2)

# Kernel density estimation for experimental data
# sns.kdeplot(data, label='Experimental Data', color='gray', linewidth=2)
plt.axvline(x=0.2, color='gray', linestyle='--', linewidth=2, label='Experimental Data (mean=0.2)')


# Add labels and title
plt.title('Comparison of Request Length Distributions')
plt.xlabel('Request Length')
plt.ylabel('Density')
plt.legend()

# Show the plot
plt.show()


# 2. Calculate mean and standard deviation for Normal and Exponential
# normal_mean = np.mean(normal_samples)
# normal_std = np.std(normal_samples)

# exponential_mean = np.mean(exponential_samples)
# exponential_std = np.std(exponential_samples)

# # 3. Plot all distributions together
# plt.figure(figsize=(12, 6))

# # Histogram for Experimental Data
# sns.histplot(data, bins=30, color='gray', label='Experimental Data', stat='density', alpha=0.5)

# # Histogram for Normal Distribution
# sns.histplot(normal_samples, bins=30, color='blue', label='Normal Distribution', stat='density', alpha=0.5)

# # Histogram for Exponential Distribution
# sns.histplot(exponential_samples, bins=30, color='red', label='Exponential Distribution', stat='density', alpha=0.5)

# # Bar plot for Uniform Distribution
# uniform_mean = np.mean(uniform_samples)
# plt.bar(uniform_mean, 0.1, width=0.05, color='green', label='Uniform Distribution', alpha=0.7)

# # Add labels and title
# plt.title('Comparison of Request Length Distributions')
# plt.xlabel('Request Length')
# plt.ylabel('Density')
# plt.legend()

# # Show the plot
# plt.xlim(0, 0.6)  # Optional: Adjust x-axis limits for better visibility
# plt.show()