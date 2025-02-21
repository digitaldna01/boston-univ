t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    cost = 0
    i = 0
    j = n // 2 
    while j <= n-1:
        cost += (a[j] - a[i])
        i += 1
        j += 1
    
    print(cost)
        