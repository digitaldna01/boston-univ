t = int(input())

while t:
    t -= 1
    s = list(input())
    flag = 1
    for i in range(len(s) - 1):
        if(s[i] == s[i+1]):
            flag = 0 
            print(1)
            break
    
    if flag == 1:
        print(len(s))
            
    
        
    