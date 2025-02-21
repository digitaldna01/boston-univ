n = int(input())
a = list(map(int, input().split()))
ans1, ans2 = 1, n
max = abs(a[0] - a[-1])
i = 0
while i < n-1:
    if (abs(a[i] - a[i + 1]) < max):
        max = abs(a[i] - a[i + 1])
        ans1 = (i + 1)
        ans2 = (i + 2)
        
    i += 1

print(ans1, ans2)