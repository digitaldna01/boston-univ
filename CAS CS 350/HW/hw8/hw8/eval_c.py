import re
import matplotlib.pyplot as plt

def extract_runtime(log_file):
    """
    Extracts the total runtime from the log file using the wall-clock time reported by the `time` utility.
    """
    with open(log_file, 'r') as file:
        for line in file:
            if "Elapsed (wall clock) time (h:mm:ss or m:ss):" in line:
                # Extract the time value
                match = re.search(r"(\d+):(\d+)\.(\d+)", line)
                if match:
                    minutes = int(match.group(1))
                    seconds = int(match.group(2))
                    milliseconds = int(match.group(3))
                    return minutes * 60 + seconds + milliseconds / 1000.0
    return None

def main():
    runtimes_a = []
    runtimes_b = []
    runtimes_c = []
    runs = list(range(1, 11))  # Run numbers 1 through 10

    for run in runs:
        log_file = f"output/a/server_run_{run}.log"
        runtime = extract_runtime(log_file)
        if runtime is not None:
            runtimes_a.append(runtime)
        else:
            print(f"Warning: Could not extract runtime for Run {run}")
    
    for run in runs:
        log_file = f"output/b/server_run_{run}.log"
        runtime = extract_runtime(log_file)
        if runtime is not None:
            runtimes_b.append(runtime)
        else:
            print(f"Warning: Could not extract runtime for Run {run}")
        
    for run in runs:
        log_file = f"output/c/server_run_{run}.log"
        runtime = extract_runtime(log_file)
        if runtime is not None:
            runtimes_c.append(runtime)
        else:
            print(f"Warning: Could not extract runtime for Run {run}")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(runs, runtimes_a, marker='o', linestyle='-', color='b', label='Total Runtime A')
    plt.plot(runs, runtimes_b, marker='s', linestyle='-', color='r', label='Total Runtime B')
    plt.plot(runs, runtimes_c, marker='^', linestyle='-', color='g', label='Total Runtime C')
    plt.title('Total Runtime vs Number of Mid Section Repeats')
    plt.xlabel('Number of Mid Section Repeats (Run Number)')
    plt.ylabel('Total Runtime (seconds)')
    plt.grid(True)
    plt.legend()
    plt.savefig("runtime_vs_repeats.png")
    plt.show()

if __name__ == "__main__":
    main()