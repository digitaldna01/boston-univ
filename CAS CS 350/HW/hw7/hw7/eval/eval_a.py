import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.linear_model import LinearRegression

def parse_server_output(filename):
    operations_data = defaultdict(list)  # Create a new dictionary
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('T0 R'):
                # Example line format:
                # T0 R1:32095109.709815,IMG_HORIZEDGES,1,0,0,32095109.709916,32095109.709995,32095109.742878,INSTR,215929516
                parts = line.strip().split(',')
                if len(parts) >= 10:
                    op_name = parts[1]
                    send_time = float(parts[6])
                    complete_time = float(parts[7])
                    duration_seconds = (complete_time - send_time)  # seconds
                    event_count = float(parts[9])
                    
                    # Add event count and duration to dictionary
                    operations_data[op_name].append([event_count, duration_seconds])
    
    return operations_data


def scatter_plot(operations_data):
    num_plots = len(operations_data)
    print(num_plots)
    cols = 3  # Number of columns per row
    rows = (num_plots + cols - 1) // cols  # Calculate number of rows needed

    plt.figure(figsize=(15, 5 * rows))  # Adjust figure size

    for i, op_name in enumerate(operations_data.keys()):
        # Separate event_count and duration
        event_counts = [data[0] for data in operations_data[op_name]]
        durations = [data[1] for data in operations_data[op_name]]

        # Create scatter plot
        plt.subplot(rows, cols, i + 1)
        plt.scatter(event_counts, durations, label=op_name, alpha=0.6)
        
        # Fit line using linear regression
        model = LinearRegression()
        model.fit(np.array(event_counts).reshape(-1, 1), durations)
        plt.plot(event_counts, model.predict(np.array(event_counts).reshape(-1, 1)), color='red', linestyle='--')

        plt.title(op_name)
        plt.xlabel('Instruction Count')
        plt.ylabel('Request Length (seconds)')
        plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    file = "result/eval_a.txt"
    operation = parse_server_output(file)
    scatter_plot(operation)
    

if __name__ == "__main__":
    main()
