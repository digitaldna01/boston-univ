t = int(input())

while t:
    t -= 1
    n, m =map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    for i in range(n-1, 0, -1):
        if a[i-1] > a[i]:
            a[i] = b[0] - a[i]
    
    flag = 0
    for i in range(n-1):
        if a[i] > a[i+1]:
            print("NO")
            flag = 1
            break
    if flag == 0:
        print("YES")
