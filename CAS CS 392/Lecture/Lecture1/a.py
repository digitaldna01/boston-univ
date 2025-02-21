t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    # print("N value : ", n)
    # print("The Array : ", a)
    l, r = 0, n-1
    ans = 0
    while l < r:
        if(a[l] == 0):
            l += 1
        elif(a[r] == 1):
            r -= 1
        else:
            ans += 1
            l += 1
            r -= 1
    print(ans)
            

