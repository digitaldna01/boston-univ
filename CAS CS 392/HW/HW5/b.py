n, x = map(int, input().split())
a = list(map(int, input().split()))

count = 0
window_sum = 0
l = 0

for r in range(n):
    window_sum += a[r]
    while ( window_sum > x and l <= r ):
        window_sum -= a[l]
        l += 1
    if window_sum == x:
        count += 1

print(count)
