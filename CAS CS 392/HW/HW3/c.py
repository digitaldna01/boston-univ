t = int(input())

while t:
    t -= 1
    n = int(input().strip())
    a = map(int, input().split())
    
    even = 0
    odd = 0
    for x in a: 
        if x % 2 == 0:
            even += x
        else:
            odd += x
    if even > odd:
        print("YES")
    else:
        print("NO")
