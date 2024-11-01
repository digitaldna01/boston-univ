import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_server_output(filename):
    operations = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('T0 R'):
                # T0 R1:2713582.267675,IMG_HORIZEDGES,1,0,0,2713582.267750,2713582.267818,2713582.293519
                # T<thread_id> R<request_id>:<send timestamp>,<operation>,<overwrite>,<client IMG ID>,<Server IMG ID>,<recv timestamp>,<start timestamp>,<complete timestamp>
                parts = line.strip().split(',')
                if len(parts) >= 8 and 'IMG_RETRIEVE' not in parts[1]:
                    op_name = parts[1]
                    # Get send timestamp from the first part (splitting by ':')
                    send_time = float(parts[6])
                    complete_time = float(parts[7])
                    duration_seconds = (complete_time - send_time) # seconds
                    operations[op_name].append(duration_seconds)
    
    return operations

def plot_cdf(data, operation, ax, title_prefix, x_max):
    if not data:
        return
    
    # 초 -> 마이크로초 변환
    sorted_data = np.sort(data) * 1_000_000  # seconds to microseconds
    yvals = np.arange(len(sorted_data))/float(len(sorted_data))
    
    # 평균과 99% tail latency 계산 (마이크로초 단위)
    avg_latency = np.mean(sorted_data)
    tail_latency = np.percentile(sorted_data, 99)
    
    ax.plot(sorted_data, yvals)
    ax.axvline(x=avg_latency, color='r', linestyle='--', 
               label=f'Avg: {avg_latency:.1f}μs')  # 소수점 한 자리까지만 표시
    ax.axvline(x=tail_latency, color='g', linestyle='--', 
               label=f'99%: {tail_latency:.1f}μs')
    
    ax.set_title(f'{title_prefix}\n{operation}')
    ax.set_xlim(0, x_max * 1_000_000)  # x_max도 마이크로초로 변환
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    ax.set_xlabel('Latency (μs)')  # 마이크로초 기호로 변경
    ax.xaxis.get_offset_text().set_fontsize(8)
    
    ax.set_ylabel('CDF')
    ax.grid(True)
    ax.legend(fontsize=8)

def main():
    # Data parsing
    small_ops = parse_server_output('Eval_b_images_small.txt')
    all_ops = parse_server_output('Eval_b_images_all.txt')
    
    # Get all operation types
    operations = list(set(small_ops.keys()) | set(all_ops.keys()))
    operations.sort()
    
    # Calculate max x value for each run
    small_max = max(max(times) for times in small_ops.values())
    all_max = max(max(times) for times in all_ops.values())
    
    # Small images plot
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Operation Latency CDFs - Small Images')
    axes = axes.flatten()
    
    for i, op in enumerate(operations):
        plot_cdf(small_ops.get(op, []), op, axes[i], 'Small Images', small_max)
    
    plt.tight_layout()
    plt.savefig('small_images_cdf.png')
    plt.close()
    
    # All images 플롯
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Operation Latency CDFs - All Images')
    axes = axes.flatten()
    
    for i, op in enumerate(operations):
        plot_cdf(all_ops.get(op, []), op, axes[i], 'All Images', all_max)
    
    plt.tight_layout()
    plt.savefig('all_images_cdf.png')
    
    # 통계 출력
    print("\nStatistics Comparison:")
    print("\nOperation | Small Images | All Images | Predictability")
    print("-" * 60)
    
    for op in operations:
        if op in small_ops and op in all_ops:
            # 초 -> 마이크로초 변환 (* 1_000_000)
            small_bcet = np.min(small_ops[op]) * 1_000_000
            small_acet = np.mean(small_ops[op]) * 1_000_000
            small_wcet = np.percentile(small_ops[op], 99) * 1_000_000
            
            all_bcet = np.min(all_ops[op]) * 1_000_000
            all_acet = np.mean(all_ops[op]) * 1_000_000
            all_wcet = np.percentile(all_ops[op], 99) * 1_000_000
            
            # 예측 가능성 계산 (WCET - BCET)
            small_pred = (small_wcet - small_bcet)
            all_pred = (all_wcet - all_bcet)
            
            print(f"\n{op}:")
            print(f"Small Images - BCET: {small_bcet:.1f}μs, ACET: {small_acet:.1f}μs, WCET: {small_wcet:.1f}μs")
            print(f"All Images - BCET: {all_bcet:.1f}μs, ACET: {all_acet:.1f}μs, WCET: {all_wcet:.1f}μs")
            print(f"Predictability (WCET-BCET) - Small: {small_pred:.1f}μs, All: {all_pred:.1f}μs")

if __name__ == "__main__":
    main()