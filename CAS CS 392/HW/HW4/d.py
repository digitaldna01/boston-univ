t = int(input())

while t:
    t -= 1
    x, y, z, k = map(int, input().split())
    count = 0
    for a in range(1, x + 1): # 1 ~ 8
        for b in range(1, min(y + 1, (k // a) + 1)): # 
            if k % (a * b) == 0: # if K is the multople of a * b"
                c = k // (a*b)
                if (a <= x and b<= y and c <= z):
                    move = (x - a + 1) * (y - b + 1) * (z - c + 1) 
                    count = max(count, move)
    print(count)