t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    l,r = 0, n-1
    flag = 0
    ans = ""
    while l <= r:
        if(flag % 2  == 0):
            print(a[l], end=" ")
            l += 1
        else:
            print(a[r], end=" ")
            r -= 1
        flag += 1 
    print()
    
    