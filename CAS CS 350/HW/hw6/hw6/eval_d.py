import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def process_log_file(filename):
    # Read the log file
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Extract operation times
    latencies = []
    for line in lines:
        if line.startswith('T0 R'):
            # T<thread_id> R<request_id>:<send timestamp>,<operation>,<overwrite>,<client IMG ID>,<Server IMG ID>,<recv timestamp>,<start timestamp>,<end timestamp>
            # Extract time information: end_time - start_time
            parts = line.split(',')
            if len(parts) >= 8:
                start_time = float(parts[6])
                end_time = float(parts[7])
                latency = end_time - start_time
                latencies.append(latency)
    
    return np.array(latencies)

def plot_cdf(data, label, output_file):
    plt.figure(figsize=(10, 6))
    
    # Calculate CDF
    sorted_data = np.sort(data)
    p = np.linspace(0, 100, len(sorted_data))
    
    # Calculate average and 99% tail latency
    avg_latency = np.mean(data)
    tail_latency = np.percentile(data, 99)
    
    # Plot CDF
    plt.plot(sorted_data * 1000, p, label='CDF')  # Convert to ms
    plt.axvline(x=avg_latency * 1000, color='r', linestyle='--', 
                label=f'Average: {avg_latency*1000:.2f}ms')
    plt.axvline(x=tail_latency * 1000, color='g', linestyle='--', 
                label=f'99% tail: {tail_latency*1000:.2f}ms')
    
    plt.xlabel('Latency (ms)')
    plt.ylabel('CDF (%)')
    plt.title(f'CDF of Image Processing Latency - {label}')
    plt.grid(True)
    plt.legend()
    
    plt.savefig(output_file)
    plt.close()

# Process each optimization level
optimization_levels = ['Eval_b_images_all', 'eval_d_O1', 'eval_d_O2']
for opt in optimization_levels:
    data = process_log_file(f'{opt}.txt')
    plot_cdf(data, f'-{opt}', f'latency_cdf_{opt}.png')