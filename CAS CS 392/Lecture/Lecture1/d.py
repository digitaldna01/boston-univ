t = int(input())

for _ in range(t):
    n = int(input())
    a = str(input())
    i, j = 0, 0
    ans = ""
    check = a[0]
    while i < n-1:
        check = a[i]
        j = i + 1
        while i < j:
            if(a[j] == check):
                ans += check
                i = j+1
            else:
                j += 1
    print(ans)
        
        