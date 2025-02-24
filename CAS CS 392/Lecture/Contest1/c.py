t = int(input())

while t:
    t -= 1
    n, k = map(int, input().split())
    s = list(input())

    l = 0
    r = n-1
    total = 0
    
    while l <= r:

        if s[l] == "W":
            l += 1
        else:
            for i in range(min(k, n-l)):
                s[l+i] = "W"

            l += k
            total += 1
    
        if s[r] == "W":
            r -= 1
        else:
            for j in range(min(k, r)):
                    s[r-j] = "W"
            r -= k
            total += 1
        
    print(total)