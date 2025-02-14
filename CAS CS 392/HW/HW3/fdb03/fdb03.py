t = int(input())

while t > 0:
    t -= 1

    n, m = map(int , input().split())
    a = list(map(int , input().split()))
    b = list(map(int , input().split()))
    b.sort()

    # prev = 0
    prev = -(2**60)
    for i in range(n):
        # Using Binary Search to find b[j] such that b[j] >= a[i] + prev.
        # DO NOT EDIT THIS! IT IS CORRECT!
        l, r = 0, m-1

        while l < r:
            mid = (l + r) // 2

            if b[mid] >= a[i] + prev:
                r = mid
            else:
                l = mid + 1
        
        # Try to minimize a[i] by setting a[i] = b[j] - a[i] while making sure that a[i] >= a[i-1]
        # check the smaller value and set each i for it first
        a[i] = min(a[i], b[l] - a[i])
        
        if (i > 0 and a[i] < a[i - 1]):
            a[i] = b[l] - a[i]
            
        prev = a[i]  

    ok = True
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            ok = False

    if ok:
        print("Yes")
    else:
        print("No")
        
        
        
        
        # if b[l] >= a[i] + prev:
        #     if (i != 0 and a[i] >= a[i-1]):
        #         a[i] = min(a[i], b[l] - a[i])
        #     else:
        #         a[i] = b[l] - a[i]

        # prev = a[i]