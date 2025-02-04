n = list(input())
m = int(input())

# Create Prefix sum
prefix_sum = [None] * (len(n) + 1)
prefix_sum[0] = 0
prefix_sum[1] = 1
for i in range(1, len(n)):
    if (n[i] == n[i-1]):
        prefix_sum[i+1] = prefix_sum[i] + 1
    else:
        prefix_sum[i+1] = prefix_sum[i]

while m:
    m -= 1
    range = list(map(int, input().split()))
    l, r = range[0], range[1]
    print(prefix_sum[r] - prefix_sum[l])
    
    
    
