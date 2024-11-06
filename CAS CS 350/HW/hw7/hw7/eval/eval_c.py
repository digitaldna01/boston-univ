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
                    # Get the number of L1MISS from the parts
                    l1_miss_count = int(parts[9])  # L1MISS 카운트는 9번째 열에 있다고 가정
                    operations[op_name].append(l1_miss_count)
    
    return operations

def plot_dis(data):
    # L1MISS 카운트를 분리
    img_blur_misses = data.get('IMG_BLUR', [])
    img_sharpen_misses = data.get('IMG_SHARPEN', [])

    # 최대값을 기준으로 빈의 범위 설정
    max_value = max(max(img_blur_misses, default=0), max(img_sharpen_misses, default=0))
    bins = np.arange(0, max_value + 1000, 5000)  # 0부터 최대값까지 1000 간격으로 설정

    plt.figure(figsize=(12, 6))

    # IMG_BLUR 분포
    count_blur, _ = np.histogram(img_blur_misses, bins=bins)
    total_blur = len(img_blur_misses)  # IMG_BLUR의 총 개수
    percentage_blur = (count_blur / total_blur) * 100 if total_blur > 0 else 0
    plt.bar(bins[:-1], percentage_blur, width=1000, alpha=0.5, label='IMG_BLUR', color='blue', align='edge')

    # IMG_SHARPEN 분포
    count_sharpen, _ = np.histogram(img_sharpen_misses, bins=bins)
    total_sharpen = len(img_sharpen_misses)  # IMG_SHARPEN의 총 개수
    percentage_sharpen = (count_sharpen / total_sharpen) * 100 if total_sharpen > 0 else 0
    plt.bar(bins[:-1] + 500, percentage_sharpen, width=1000, alpha=0.5, label='IMG_SHARPEN', color='orange', align='edge')

    # x축 범위 설정
    plt.xlim(left=0, right=max_value + 1000)  # x축의 범위를 설정하여 데이터가 있는 부분만 확대

    plt.title('Percentage Distribution of L1MISS Counts')
    plt.xlabel('L1MISS Count Bins')
    plt.ylabel('Percentage of Total Requests (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('l1miss_distribution.png')
    plt.show()
    

def main():
    # Data parsing
    data = parse_server_output('result/eval_c.txt')
    
    # Plot distributions
    plot_dis(data)

if __name__ == "__main__":
    main()