import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_server_output(filename):
    operations = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('T0 R'):
                parts = line.strip().split(',')
                if len(parts) >= 10:  # 10개 이상의 요소가 있어야 함
                    op_name = parts[1]  # Operation name
                    # Get the number of LL cache misses from the parts
                    ll_cache_misses = int(parts[9])  # Assuming the cache miss count is in the 10th column
                    operations[op_name].append(ll_cache_misses)
    
    return operations

def plot_cdf_for_operations(run1_data, run2_data):
    # 모든 작업 유형 가져오기
    operations = list(set(run1_data.keys()) | set(run2_data.keys()))
    
    num_plots = len(operations)
    cols = 3
    rows = (num_plots + cols - 1) // cols  # Calculate number of rows needed

    plt.figure(figsize=(15, 5 * rows))  # Adjust figure size

    for i, op in enumerate(operations):
        plt.subplot(rows, cols, i + 1)
        
        # RUN1 데이터
        if op in run1_data:
            sorted_data1 = np.sort(run1_data[op])
            yvals1 = np.arange(len(sorted_data1)) / float(len(sorted_data1))
            plt.plot(sorted_data1, yvals1, label=f'Run 1 - {op}', linestyle='-', color='blue')

            # 평균 수치 표시
            avg_misses1 = np.mean(sorted_data1)
            plt.axvline(x=avg_misses1, color='blue', linestyle='--', label=f'Avg Run 1 - {op}: {avg_misses1:.1f}')

        # RUN2 데이터
        if op in run2_data:
            sorted_data2 = np.sort(run2_data[op])
            yvals2 = np.arange(len(sorted_data2)) / float(len(sorted_data2))
            plt.plot(sorted_data2, yvals2, label=f'Run 2 - {op}', linestyle='-', color='orange')

            # 평균 수치 표시
            avg_misses2 = np.mean(sorted_data2)
            plt.axvline(x=avg_misses2, color='orange', linestyle='--', label=f'Avg Run 2 - {op}: {avg_misses2:.1f}')

        plt.title(f'CDF of LL Cache Misses for {op}')
        plt.xlabel('Number of LL Cache Misses')
        plt.ylabel('CDF')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    # Data parsing
    run1 = parse_server_output('result/eval_b_run1.txt')
    run2 = parse_server_output('result/eval_b_run2.txt')
    
    # Plot CDF for each operation
    plot_cdf_for_operations(run1, run2)
    
    # 통계 출력
    print("\nStatistics Comparison:")
    print("\nOperation | Run 1 (Min, Max) | Run 2 (Min, Max)")
    print("-" * 60)
    
    # 모든 작업 유형 가져오기
    operations = list(set(run1.keys()) | set(run2.keys()))
    operations.sort()
    
    for op in operations:
        small_min = np.min(run1[op]) if op in run1 else 'N/A'
        small_max = np.max(run1[op]) if op in run1 else 'N/A'
        all_min = np.min(run2[op]) if op in run2 else 'N/A'
        all_max = np.max(run2[op]) if op in run2 else 'N/A'
        
        print(f"{op}: Run 1 - Min: {small_min}, Max: {small_max} | Run 2 - Min: {all_min}, Max: {all_max}")

if __name__ == "__main__":
    main()