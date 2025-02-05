t = list(map(int, input().split()))
n, q = t[0], t[1]
x = list(map(int, input().split()))

# prefix sum x 
prefix_x = [None] * (n+1)
prefix_x[0] = 0
for i in range(n):
    prefix_x[i+1] = prefix_x[i] + x[i]

while q:
    q -= 1
    query = list(map(int, input().split()))
    a, b = query[0], query[1]
    print(prefix_x[b] - prefix_x[a-1])