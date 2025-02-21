t = int(input())

def fun(n, x):
    count = 0
    for a in range(1, x - 1):
        for b in range(1, (n // a) + 1):
            count += max(0, min( x-a-b, ((n - a * b) // (a+b))))
    return count

while t:
    t -= 1
    n, x = map(int, input().split())
    print(fun(n, x))
    

