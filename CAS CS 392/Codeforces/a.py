t = int(input())

while t:
    t -= 1
    singular = input()
    index = -1
    for i in range(len(singular) - 1 ):
        if (singular[i] == "u" and singular[i+1] == "s"):
            index = i
    
    print(singular[:i] + "i")