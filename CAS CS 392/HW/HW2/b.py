t = list(map(int, input().split()))
n, q = t[0], t[1]
p = list(map(int, input().split()))
p.sort(reverse=True)
prefix_p = [None] * (n + 1)
prefix_p[0] = 0
for i in range(n):
    prefix_p[i+1] = prefix_p[i] + p[i]

while q:
    q -= 1
    query = list(map(int, input().split()))
    x, y = query[0], query[1]
    print(prefix_p[x] - prefix_p[x-y])
    