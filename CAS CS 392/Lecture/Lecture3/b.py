t = int(input())

while t:
    t -= 1
    n, W = map(int, input().split())
    items = list(map(int, input().split()))
    
    stack = []
    for i in range(n):
        stack.append(items[i])
    
    stack.sort(reverse=True)
    num = -1
    weight = 0
    count = 0
    needWeight = 0
    indexs = []
    for i in range(n):
        # print("Need weight", needWeight)
        if stack[i] <= W - needWeight :
            needWeight += stack[i]
            count += 1
            for j in range(n):
                if items[j] == stack[i]:
                    indexs.append(j+1)
                    items[j] = -1
                    break
            
            
        if ( W // 2 <= needWeight <= W):
            num = count
            break
        
    print(num)
    if (num != -1):
        for j in range(len(indexs)):
            print(indexs[j], end=" ")
        print()
    