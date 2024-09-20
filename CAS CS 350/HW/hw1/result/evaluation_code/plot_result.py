import numpy as np
import matplotlib.pyplot as plt

# Initialize an empty list to store the numeric results
data = []

# Read the combined_output.txt file
with open('./complete-send/a12_stat.txt', 'r') as f:
    for line in f:
        # Assuming that the program output is numeric and we only want those lines
        try:
            # Attempt to convert each line to a float
            num = float(line.strip())
            data.append(num)
        except ValueError:
            # Ignore lines that don't contain numeric data (e.g., "Run completed" or separators)
            continue

# Convert the collected data to a numpy array
data_array = np.array(data)

# Generate x-axis values corresponding to seconds (1s to 10s)
x_values = np.arange(1, len(data_array) + 1)

# Calculate statistics
min_value = np.min(data_array)
max_value = np.max(data_array)
mean_value = np.mean(data_array)
std_value = np.std(data_array)

# Print statistics
print(f"Min: {min_value}")
print(f"Max: {max_value}")
print(f"Mean: {mean_value}")
print(f"Standard Deviation: {std_value}")

# Create a plot of the data points
plt.figure(figsize=(10, 6))
plt.plot(x_values, data_array, marker='o', linestyle='-', label='Data points')

# Add a horizontal line for the mean value
plt.axhline(mean_value, color='r', linestyle='--', label=f'Mean: {mean_value:.2f} MHz')

# Add title and labels
plt.title('-a 10 Max, Min, Mean, STD Deviation')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency (MHz)')

# Display statistics on the plot
plt.text(0.1, 0.9, f'Min: {min_value}', transform=plt.gca().transAxes)
plt.text(0.1, 0.85, f'Max: {max_value}', transform=plt.gca().transAxes)
plt.text(0.1, 0.8, f'Mean: {mean_value}', transform=plt.gca().transAxes)
plt.text(0.1, 0.75, f'Std Dev: {std_value}', transform=plt.gca().transAxes)

# Set x-axis ticks to match the data points
plt.xticks(x_values)

# Show the plot with data points
plt.legend()
plt.grid(True)

# Save the plot as an image file
plt.savefig('program_output_plot.png')  # Save as PNG file
print("Plot saved as 'program_output_plot.png'")

# Optionally, display the plot
plt.show()