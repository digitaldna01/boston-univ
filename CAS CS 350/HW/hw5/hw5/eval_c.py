import os
import re
import numpy as np
import matplotlib.pyplot as plt

def parse_file(filepath):
    response_times = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('T'):
                parts = line.split(':')[1].split(',')
                send_timestamp = float(parts[0])
                complete = float(parts[4])
                response_time = complete - send_timestamp
                response_times.append(response_time)

    return np.array(response_times)

def plot_cdf(response_times, policy, output_file, max_time):
    sorted_times = np.sort(response_times)
    y = np.arange(1, len(sorted_times) + 1) / len(sorted_times)

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_times, y, label=f'{policy} CDF')
    plt.xlabel('Response Time (seconds)')
    plt.ylabel('Cumulative Probability')
    plt.title(f'CDF of Response Times for {policy}')
    plt.grid(True)

    # 평균 응답 시간
    avg_response_time = np.mean(response_times)
    plt.axvline(x=avg_response_time, color='r', linestyle='--', label=f'Average ({avg_response_time:.4f}s)')

    # 99번째 백분위수
    percentile_99 = np.percentile(response_times, 99)
    plt.axvline(x=percentile_99, color='g', linestyle='--', label=f'99th Percentile ({percentile_99:.4f}s)')

    plt.legend()
    plt.xlim(0, max_time)
    plt.ylim(0, 1)
    plt.savefig(output_file)
    plt.close()

    return avg_response_time, percentile_99

# 디렉토리 설정
directory = "result/result_b"

# FIFO와 SJN의 10번째 실행 파일 찾기
fifo_file = None
sjn_file = None

for filename in os.listdir(directory):
    if filename.startswith("FIFO_40_"):
        fifo_file = os.path.join(directory, filename)
    elif filename.startswith("SJN_40_"):
        sjn_file = os.path.join(directory, filename)

if fifo_file and sjn_file:
    fifo_times = parse_file(fifo_file)
    sjn_times = parse_file(sjn_file)

    # 두 데이터셋의 최대값 중 큰 값을 x축의 최대값으로 사용
    max_time = max(np.max(fifo_times), np.max(sjn_times))

    fifo_avg, fifo_99 = plot_cdf(fifo_times, "FIFO", "fifo_cdf.png", max_time)
    sjn_avg, sjn_99 = plot_cdf(sjn_times, "SJN", "sjn_cdf.png", max_time)

    print(f"FIFO - Average: {fifo_avg:.4f}s, 99th Percentile: {fifo_99:.4f}s")
    print(f"SJN - Average: {sjn_avg:.4f}s, 99th Percentile: {sjn_99:.4f}s")
else:
    print("Could not find the 10th run files for FIFO and/or SJN.")
