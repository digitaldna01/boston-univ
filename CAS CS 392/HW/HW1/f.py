n = int(input())
boys = list(map(int,input().split()))
m = int(input())
girls = list(map(int,input().split()))

boys.sort()
girls.sort()

i = 0
l = 0
max = 0

while i < n:
    for j in range(l, m):
        if (-1 <= boys[i] - girls[j] <= 1):
            max +=1
            l = j+1
            break
    i += 1

print(max)
    