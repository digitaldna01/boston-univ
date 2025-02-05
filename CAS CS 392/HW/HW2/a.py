t = int(input())

while t:
    t -= 1
    n = int(input())
    r = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    
    prefix_a = [None] * (n+1)
    prefix_b = [None] * (m+1)
    
    prefix_a[0] = 0
    prefix_b[0] = 0
    
    #prefix_a
    for i in range(n):
        prefix_a[i+ 1] = prefix_a[i] + r[i]
    
    #prefix_b
    for i in range(m):
        prefix_b[i+ 1] = prefix_b[i] + b[i]
        
    a_max = max(prefix_a)
    b_max = max(prefix_b)
    
    print(a_max + b_max)