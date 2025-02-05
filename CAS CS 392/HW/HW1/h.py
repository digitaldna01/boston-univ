t = int(input())

while t:
    t -= 1
    n = list(map(int, input()))
    flag = 1
    while flag > 0:
        flag = 0
        i = 0
        print(n)
        while i < len(n) - 1:
            if (i > 0 and n[i-1] % 2 == n[i] % 2 and n[i] % 2 != n[i+1] % 2 and n[i-1] > n[i+1]):
                temp = n[i]
                n[i] = n[i+1]
                n[i+1] = temp
                flag = 1 
            elif (n[i] % 2 != n[i+1] % 2 and n[i] > n[i+1]):
                temp = n[i]
                n[i] = n[i+1]
                n[i+1] = temp
                flag = 1 
            i += 1
    
    for j in range(len(n)):
        print(n[j], end="")
    print()
