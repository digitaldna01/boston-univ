t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    i = 0
    ans = 0
    while i < n:
        if(a[i] > b[i]):    
            a.append(b[i])    
            a.sort()
            ans += 1
        i+=1
        
    print(ans)
            
