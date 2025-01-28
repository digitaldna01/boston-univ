t = str(input())
n = len(t)
i = 0
j = 1
count = 1
num = 1
while j < n:
    char = t[i]
    if(char == t[j]):
        num += 1
        j += 1
    else:
        i = j
        j = i + 1
        num = 1
        
    if num > count:
        count = num

print(count)
        