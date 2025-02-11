n, k = map(int, input().split())
s = list(map(int, input()))

def changes(n, k):
    if k == 0:
        return(int("".join(map(str, s))))
    if n == 1:
        return(0)
    
    if (s[0] == 1):
        l = 1  
    else:  
        s[0] = 1
        k -= 1
        l = 1

    while l < n:
        if (s[l] != 0 and k > 0):
            s[l] = 0
            l += 1
            k -=1
        else:
            l += 1

    return(int("".join(map(str, s))))

print(changes(n, k))