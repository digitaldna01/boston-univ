# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns

# # R<request ID>:<sent timestamp>,<request length>,<receipt timestamp>,<start timestamp>,<completion timestamp>
# # X<request ID>:<sent timestamp>,<request length>,<reject timestamp>

# # Open the file and read the content
# with open('.//result/result_b.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
#     lines = file.readlines()

# # define the data array set
# data = []

# #### Preprocessing the data
# for line in lines:
#     line = line.strip()
    
#     if line.startswith("R"):
#         parts = line.split(',')
#         lengths = float(parts[1])
        
#         # Add append the data set with each lengths of the request
#         data.append(lengths)

# # 1. Generate samples from the theoretical distributions
# num_samples = 10000

# # Normal distribution
# normal_samples = np.random.normal(loc=1/5, scale=1, size=num_samples) # mean 1/10

# # Exponential distribution
# exponential_samples = np.random.exponential(scale=1/5, size=num_samples) # mean 1/10

# # Uniform distribution
# uniform_samples = np.random.uniform(low=0, high=2/5, size=num_samples)  # Mean 1/10

# # 2. Plot all distributions together
# plt.figure(figsize=(12, 6))

# # Kernel density estimation for Normal distribution
# sns.kdeplot(normal_samples, label='Normal Distribution', color='blue', linewidth=2)

# # Kernel density estimation for Exponential distribution
# sns.kdeplot(exponential_samples, label='Exponential Distribution', color='red', linewidth=2)

# # # Plotting the histogram for experimental data
# # sns.histplot(data, bins=30, color='gray', kde=False, label='Experimental Data', stat='density', alpha=0.5)

# # Kernel density estimation for Uniform distribution
# sns.kdeplot(uniform_samples, label='Uniform Distribution', color='green', linewidth=2)

# # Kernel density estimation for experimental data
# sns.kdeplot(data, label='Experimental Data', color='gray', linewidth=2)
# # plt.axvline(x=0.2, color='gray', linestyle='--', linewidth=2, label='Experimental Data (mean=0.2)')


# # Add labels and title
# plt.title('Comparison of Request Length Distributions of -d 2')
# plt.xlabel('Request Length')
# plt.ylabel('Density')
# plt.legend()

# # Show the plot
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Open the file and read the content
with open('.//result/result_b.txt', 'r') as file:
    lines = file.readlines()

# Define the data array set
data = []

# Preprocess the data
for line in lines:
    line = line.strip()
    
    if line.startswith("R"):
        parts = line.split(',')
        lengths = float(parts[1])
        
        # Add append the data set with each length of the request
        data.append(lengths)

# Convert data to a NumPy array for easier manipulation
data = np.array(data)

# Calculate the mean and standard deviation of the experimental data
data_mean = np.mean(data)
data_std = np.std(data)

print(f"Mean of experimental data: {data_mean}")
print(f"Standard deviation of experimental data: {data_std}")

# Generate samples from the theoretical distributions
num_samples = 10000

# Normal distribution (mean = data_mean, std = data_std)
normal_samples = np.random.normal(loc=data_mean, scale=data_std, size=num_samples)

# Exponential distribution with mean = data_mean. The parameter 'scale' is equivalent to the mean of the exponential distribution.
exponential_samples = np.random.exponential(scale=data_mean, size=num_samples)

# Uniform distribution with mean = data_mean. For a uniform distribution, mean = (a + b) / 2.
# So, set 'a' and 'b' such that their mean is data_mean.
uniform_range = data_mean * 2  # Assuming symmetric interval around data_mean
uniform_samples = np.random.uniform(low=0, high=uniform_range, size=num_samples)

# Plot all distributions together
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
plt.title('Comparison of Request Length Distributions of -d 2')
plt.xlabel('Request Length')
plt.ylabel('Density')
plt.legend()

# Show the plot
plt.show()
