t = int(input())

while t:
    t -= 1
    query = list(map(int, input().split()))
    n, q = query[0], query[1]
    a = list(map(int, input().split()))
    
    prefix_a = [None] * (n+1)
    prefix_a[0] = 0
    # Fill prefix a
    for i in range(n):
        prefix_a[i + 1] = prefix_a[i] + a[i]
    
    while q:
        q -= 1
        case = list(map(int, input().split()))
        l, r, k = case[0], case[1], case[2]
        new = (prefix_a[-1] - prefix_a[r] + prefix_a[l-1])
        replace = ((r - l + 1) * k)
        if ((new + replace) % 2 == 1):
            print("YES")
        else:
            print("NO")