t = int(input())

while t:
    t -= 1
    m, a, b, c = map(int, input().split())
    total = 0
    rest = 0
    if(m - a >= 0):
        total += a
        rest += m - a
    else:
        total += m
        rest += 0

    
    if(m - b >= 0):
        total += b
        rest += m - b
    else:
        total += m
        rest += 0

    if (rest - c >= 0):
        total += c
    else:
        total += rest


    print(total)
    