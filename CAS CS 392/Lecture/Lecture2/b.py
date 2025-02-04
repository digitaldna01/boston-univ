n = int(input())
cost = list(map(int, input().split()))

#prefix sum
prefix_sum = [None] * (n + 1)
prefix_sum[0] = 0

for i in range(n):
    prefix_sum[i+1] = prefix_sum[i] + cost[i]

#Nondescending order
cost.sort()
sorted_prefix_sum = [None] * (n + 1)
sorted_prefix_sum[0] = 0
for i in range(n):
    sorted_prefix_sum[i+1] = sorted_prefix_sum[i] + cost[i]

m = int(input())
while m:
    m -= 1
    question = list(map(int, input().split()))
    type = question[0]
    l = question[1]
    r = question[2]
    
    if type == 1:
        print(prefix_sum[r] - prefix_sum[l-1])
    else:
        print(sorted_prefix_sum[r] - sorted_prefix_sum[l-1])