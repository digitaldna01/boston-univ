import matplotlib.pyplot as plt
import numpy as np

# Data from the provided information
arrival_rates = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'a12']
utilization = [7.992457068, 15.98208316, 23.96548751, 31.94978129, 39.93161284, 
               47.91159135, 55.88884212, 63.79303445, 71.58894635, 79.29018026, 
               86.9435017, 94.54896029]

# Numerical representation of 'a1' to 'a12'
a_values = np.array([0.08135870600678027, 0.08135665401164442, 0.08133770802989602, 0.0813375960085541, 0.08133682199567556, 0.08133660998102278, 0.08133548799622804, 0.08133544398937374, 0.08133439399953932, 0.08133324399311095, 0.08133226200006902, 0.08133184199780226])
utilization_values = np.array(utilization)
# Calculate the Pearson correlation coefficient
correlation_coefficient = np.corrcoef(a_values, utilization_values)[0, 1]
print(correlation_coefficient)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(utilization,a_values,  marker='o', linestyle='-', color='b')
# plt.plot(arrival_rates, utilization, marker='o', linestyle='-', color='b')

# Labels and title
plt.ylabel('Average response time')
plt.xlabel('Server Utilization (Percentage)')
plt.title('Server Utilization vs. -a Parameter')

# Show the plot
plt.grid(True)
plt.show()

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Data from the provided information
arrival_rates = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'a12']


utilization = [7.992457068, 15.98208316, 23.96548751, 31.94978129, 39.93161284, 47.91159135, 55.88884212, 63.79303445, 71.58894635, 79.29018026, 86.9435017, 94.54896029]

# Numerical representation of 'a1' to 'a12'
a_values = np.array([0.08135870600678027, 0.08135665401164442, 0.08133770802989602, 0.0813375960085541, 0.08133682199567556, 0.08133660998102278, 0.08133548799622804, 0.08133544398937374, 0.08133439399953932, 0.08133324399311095, 0.08133226200006902, 0.08133184199780226])
utilization_values = np.array(utilization)

# Smooth the data using cubic spline interpolation
# Define 300 points between the min and max of utilization for a smooth curve
# x_smooth = np.linspace(utilization_values.min(), utilization_values.max(), 300)

# Create a spline function
# spl = make_interp_spline(utilization_values, a_values, k=3)  # k=3 for cubic spline

# Get the smooth y values (a_values)
# y_smooth = spl(x_smooth)

# Plotting the data
plt.figure(figsize=(10, 6))
# plt.plot(x_smooth, y_smooth, color='b', label='Smooth Curve')  # smooth curve
plt.scatter(utilization_values, a_values, color='r', label='Data Points')  # actual data points

# Labels and title
plt.ylabel('Average response time')
plt.xlabel('Server Utilization (Percentage)')
plt.title('Server Utilization vs. -a Parameter')

# Grid and legend
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

