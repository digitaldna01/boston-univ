import math

t = int(input())

while t:
    t -= 1
    n = int(input())
    a = list(map(int, input().split()))
    
    num = 0
    for i in range(n-2, -1, -1):
        if a[i] > a[i + 1]:
            p = math.ceil(a[i] / a[i+1]) - 1
            num += p
            a[i] = a[i] // (p+1)
        
    print(num)
