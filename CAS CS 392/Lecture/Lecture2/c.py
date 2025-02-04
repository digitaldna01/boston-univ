m = int(input())

while m:
    m -= 1
    length = list(map(int, input().split()))
    n, k = length[0], length[1]
    letter = list(input())
    
    # make the prefix cheksum based on how many b are in the arrays.
    prefix_sum = [None] * (n+1)
    prefix_sum[0] = 0
    for i in range(n):
        if (letter[i] == "W"):
            prefix_sum[i+1] = prefix_sum[i] + 1
        else:
            prefix_sum[i+1] = prefix_sum[i]
    max = n
    for i in range(k, n+1):
        if (prefix_sum[i] - prefix_sum[i-k] < max):
            max = prefix_sum[i] - prefix_sum[i-k]
    print(max)
    
        