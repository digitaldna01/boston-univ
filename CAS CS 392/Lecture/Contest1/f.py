t = int(input())  

while t:
    t -= 1
    n, x = map(int, input().split())  
    a = list(map(int, input().split())) 
    
    copy = a[:]  
    # print(copy)
    # sort first non decrasing order
    copy.sort()
    flag = True  
    
    # can't move x number variables
    for i in range(n - x, x):
        if a[i] != copy[i]:
            flag = False
            break  
        
    if flag:
        print("YES")
    else:
        print("NO")
