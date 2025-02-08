t = int(input())

for _ in range(t):
    nk = list(map(int, input().split()))
    n, k = nk[0], nk[1]
    s = list(map(int, input().split()))
    difference = n - k
    #reverse prefix
    re_prefix = [0] * (k)
    re_prefix[0] = s[0]
    flag = 0
    max = s[0] / (difference+1)
    
    for i in range(k-1):
        if (s[i+1] - s[i] >= max):
            max = s[i+1] - s[i]
        else:
            flag = 1
            print("No")
            break
    if(flag == 0):
        print("yes")
        
        
        
        
        
        
        
