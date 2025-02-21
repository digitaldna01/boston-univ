t = int(input())

while t:
    t -= 1
    n = int(input())
    s = str(input())

    count = 0
    min_count = 0

    for c in s:
        if c == ")":
            count += 1
        else:
            count -= 1
        
        count = min(count, min_count)

    print(abs(count))