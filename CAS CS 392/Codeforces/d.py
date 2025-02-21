t = int(input())

while t:
    t -= 1
    n, m = map(int, input().split())
    arrays = []
    
    for _ in range(n):
        a = list(map(int, input().split()))
        arrays.append(a)
    print(arrays)
    
    arrays.sort(key=lambda x: (sum(x), x))
    
    print(arrays)
    prefix_arr = []
    for array in arrays:
        prefix_a = [0] * (m + 1)
        for i in range(m):
            prefix_a[i+1] = prefix_a[i] + array[i]
        prefix_arr.append(prefix_a)

    print(prefix_arr)
    prefix_arr.sort(key=lambda x : )
    print()