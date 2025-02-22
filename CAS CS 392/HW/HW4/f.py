t = int(input())

while t:
    t -= 1
    n = int(input())
    s = list(map(int, input().strip()))
    
    consecutiveOne, consecutiveZero = 0,0
    maxConsecutiveOne, maxConsecutiveZero = 0,0
    totalOne, totalZero = 0,0
    
    for digit in s:
        if digit == 1:
            consecutiveOne += 1
            maxConsecutiveOne = max(consecutiveOne, maxConsecutiveOne)
            totalOne += 1
        else:
            consecutiveOne = 0 # reset consective ones

        if digit == 0:
            consecutiveZero += 1
            maxConsecutiveZero = max(consecutiveZero, maxConsecutiveZero)
            totalZero += 1
        else:
            consecutiveZero = 0
    x2, y2, xy = maxConsecutiveOne**2, maxConsecutiveZero**2, totalOne * totalZero
    maxCost = max(x2, y2, xy)
    print(maxCost)