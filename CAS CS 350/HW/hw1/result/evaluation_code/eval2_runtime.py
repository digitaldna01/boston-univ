# Open the file and read the content
with open('./server_result/server_result_a12.txt', 'r') as file:  # Replace 'timestamps.txt' with your file name
    lines = file.readlines()

# Initialize a variable to hold the sum
total_seconds = 0.0

# Loop through each line
for line in lines:
    # Split the line by commas to extract the second timestamp (second value)
    parts = line.split(',')
    second_timestamp = float(parts[3]) - float(parts[2])  # Extract the completion and recipt timestamp and subtract
    
    # Add to the total
    total_seconds += second_timestamp

# Print the total sum
print(f"Total sum of second timestamps: {total_seconds}")

