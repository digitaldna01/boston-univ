import matplotlib.pyplot as plt
import numpy as np

# Data for the two methods
time_labels = ['Sunday Morning', 'Sunday Afternoon', 'Monday Morning', 'Monday Afternoon', 'Tuesday Morning', 'Tuesday Afternoon', 'Wednesday Morning', 'Wednesday Afternoon', 'Thursday Morning', 'Thursday Afternoon']
nanosleep_freqs = [2893.210690, 2893.226345, 2793.471372, 2599.981557, 2793.459690, 2793.459890, 2793.455472, 2793.457106, 2793.434154, 2599.978443]
busywait_freqs = [2893.190558, 2893.190553, 2793.434384, 2599.963650, 2793.421919, 2793.418744, 2793.418386, 2793.419676, 2793.415095, 2599.959175]

# Time (x-axis) as numerical values for plotting
x = np.arange(len(time_labels))

# Plotting the updated graph
plt.figure(figsize=(10, 6))

# Plot nanosleep with thicker line and bigger markers
plt.plot(x, nanosleep_freqs, marker='o', markersize=8, linestyle='-', linewidth=2, color='b', label='Nanosleep Method')
# Plot busywait with thicker line and bigger markers
plt.plot(x, busywait_freqs, marker='o', markersize=8, linestyle='-', linewidth=2, color='r', label='Busywait Method')

# Adding labels and title
plt.title('Clock Frequency Measurements using Nanosleep and Busywait Methods (Enhanced)')
plt.xlabel('Time of Measurement')
plt.ylabel('Clock Frequency (MHz)')
plt.xticks(x, time_labels, rotation=45)
plt.legend()

# Grid for better readability
plt.grid(True)

# Show updated plot
plt.tight_layout()
plt.show()

# Correlation calculation
correlation = np.corrcoef(nanosleep_freqs, busywait_freqs)[0, 1]

# Plotting correlation graph
plt.figure(figsize=(8, 6))

# Scatter plot to show relationship
plt.scatter(nanosleep_freqs, busywait_freqs, color='purple')

# Best fit line
m, b = np.polyfit(nanosleep_freqs, busywait_freqs, 1)
plt.plot(nanosleep_freqs, m*np.array(nanosleep_freqs) + b, color='green', linestyle='--', label=f'Best Fit Line\nCorrelation: {correlation:.4f}')

# Adding labels and title for correlation graph
plt.title('Correlation between Nanosleep and Busywait Methods')
plt.xlabel('Nanosleep Clock Frequency (MHz)')
plt.ylabel('Busywait Clock Frequency (MHz)')
plt.legend()

# Show scatter plot
plt.tight_layout()
plt.show()

correlation
