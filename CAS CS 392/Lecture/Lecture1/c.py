n = int(input())
a = list(map(int, input().split()))
l, r = 0, n-1
sereja, dima = 0, 0
flag = 0
while l <= r:
    if(a[l] > a[r]):
        if(flag % 2 == 0):
            sereja += a[l]
        else:
            dima += a[l]
        l += 1
    else:
        if(flag % 2 == 0):
            sereja += a[r]
        else:
            dima += a[r]
        r -= 1
    flag += 1

print(sereja, dima)