import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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

# 1. Generate samples from the theoretical distributions
num_samples = 10000

# Normal distribution
normal_samples = np.random.normal(loc=1/10, scale=1, size=num_samples) # mean 1/10

# Exponential distribution
exponential_samples = np.random.exponential(scale=1/10, size=num_samples) # mean 1/10

# Uniform distribution
uniform_samples = np.random.uniform(low=0, high=0.2, size=num_samples)  # Mean 1/10

# 2. Plot all distributions together
plt.figure(figsize=(12, 6))

# Kernel density estimation for Normal distribution
sns.kdeplot(normal_samples, label='Normal Distribution', color='blue', linewidth=2)

# Kernel density estimation for Exponential distribution
sns.kdeplot(exponential_samples, label='Exponential Distribution', color='red', linewidth=2)

# Kernel density estimation for Uniform distribution
sns.kdeplot(uniform_samples, label='Uniform Distribution', color='green', linewidth=2)

# Kernel density estimation for experimental data
sns.kdeplot(data, label='Experimental Data', color='gray', linewidth=2)

# Add labels and title
plt.title('Comparison of Request Length Distributions')
plt.xlabel('Request Length')
plt.ylabel('Density')
plt.legend()

# Show the plot
plt.show()