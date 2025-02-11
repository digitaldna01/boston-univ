import math
t = int(input())

while t:
    t -= 1
    n = int(input())
    a, b = n, n-1
    print(2)
    while n - 1:
        n -= 1
        print(a, b)
        a = math.ceil((a + b) / 2)
        b  -= 1