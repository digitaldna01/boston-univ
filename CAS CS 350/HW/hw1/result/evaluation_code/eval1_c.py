import matplotlib.pyplot as plt
import numpy as np

# Data for the two methods
time_labels = ['Sunday Morning', 'Sunday Afternoon', 'Monday Morning', 'Monday Afternoon', 'Tuesday Morning', 'Tuesday Afternoon']
nanosleep_freqs = [2893.210690, 2893.226345, 2793.471372, 2599.981557, 2793.459690, 2793.459890]
busywait_freqs = [2893.190558, 2893.190553, 2793.434384, 2599.963650, 2793.421919, 2793.418744]

# Time (x-axis) as numerical values for plotting
x = np.arange(len(time_labels))

# Plotting
plt.figure(figsize=(10, 6))

# Plot nanosleep
plt.plot(x, nanosleep_freqs, marker='o', linestyle='-', color='b', label='Nanosleep Method')
# Plot busywait
plt.plot(x, busywait_freqs, marker='o', linestyle='-', color='r', label='Busywait Method')

# Adding labels and title
plt.title('Clock Frequency Measurements using Nanosleep and Busywait Methods')
plt.xlabel('Time of Measurement')
plt.ylabel('Clock Frequency (MHz)')
plt.xticks(x, time_labels, rotation=45)
plt.legend()

# Grid for better readability
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
