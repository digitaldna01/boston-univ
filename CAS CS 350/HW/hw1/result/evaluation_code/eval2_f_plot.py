import matplotlib.pyplot as plt
import numpy as np

# Data from the provided information
utilization = [7.992457068, 15.98208316, 23.96548751, 31.94978129, 39.93161284, 47.91159135, 55.88884212, 63.79303445, 71.58894635, 79.29018026, 86.9435017, 94.54896029]

# Numerical representation of 'a1' to 'a12'
a_values = np.array([0.08694804399926215, 0.09574253800325096, 0.10481401402223856, 0.11513752001337707, 0.12865784599632024, 0.1452020660014823, 0.16844792199973016, 0.1977727539902553, 0.25022777199279517, 0.3287245159978047, 0.44226453801058235, 1.118266559992917])
utilization_values = np.array(utilization)


# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(utilization, a_values,  marker='o', linestyle='-', color='b')
# plt.plot(arrival_rates, utilization, marker='o', linestyle='-', color='b')

# Labels and title
plt.ylabel('Average Response Time')
plt.xlabel('Server Utilization (Percentage)')
plt.title('Server Utilization vs. Average Response Time')

# Show the plot
plt.grid(True)
plt.show()

