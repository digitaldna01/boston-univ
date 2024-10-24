import os
import re

def parse_time(time_str):
    # Handle "h:mm:ss" or "m:ss" format
    parts = time_str.split(':')
    if len(parts) == 3:  # h:mm:ss format
        h, m, s = map(float, parts)
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:  # m:ss format
        m, s = map(float, parts)
        return m * 60 + s
    else:
        raise ValueError(f"Unexpected time format: {time_str}")

def get_elapsed_times(directory, policy):
    times = []
    pattern = rf"{policy}_\d+_result\.txt"
    
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for line in reversed(lines):  # Read the file in reverse order
                    if "Elapsed (wall clock) time" in line:
                        time_str = line.split('):')[1].strip()
                        try:
                            time = parse_time(time_str)
                            times.append(time)
                        except ValueError as e:
                            print(f"Error parsing time in {filename}: {e}")
                        break
    return times

directory = "result/result_a/high"
fifo_times = get_elapsed_times(directory, "FIFO")
sjn_times = get_elapsed_times(directory, "SJN")

# Calculate averages
fifo_avg = sum(fifo_times) / len(fifo_times) if fifo_times else 0
sjn_avg = sum(sjn_times) / len(sjn_times) if sjn_times else 0

print(f"FIFO Times: {fifo_times}")
print(f"SJN Times: {sjn_times}")
print(f"FIFO average execution time: {fifo_avg:.2f} seconds")
print(f"SJN average execution time: {sjn_avg:.2f} seconds")

# Compare results
if fifo_avg < sjn_avg:
    print(f"FIFO is {sjn_avg - fifo_avg:.2f} seconds faster than SJN.")
elif sjn_avg < fifo_avg:
    print(f"SJN is {fifo_avg - sjn_avg:.2f} seconds faster than FIFO.")
else:
    print("FIFO and SJN have the same execution time.")
