t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input()))
    l, r = 0, n-1
    pair = 0
    while l < r:
        if(a[l] != a[r]):
            pair += 2
        else:
            break
        l += 1
        r -= 1
    print(n - pair)