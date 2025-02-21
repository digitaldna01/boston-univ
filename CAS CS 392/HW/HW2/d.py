t = int(input())

while t:
    t -= 1
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    p = [0] * (n + 1)
    for i in range(1, n-1):
        if (a[i]> a[i-1] and a[i] > a[i+1]):
            p[i] = 1 + p[i-1]
        else:
            p[i] = p[i-1]

    

    max = -1
    index = -1
    for j in range(n - k + 1):
        if (p[j + k - 2] - p[j] > max):
            max = p[j + k - 2] - p[j]
            index = j
            
    print(max + 1, index + 1)