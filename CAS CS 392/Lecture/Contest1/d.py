n, m, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

a.sort()
b.sort()

def distribution(n, m, k, a, b):
    count = 0
    l = 0
    r = 0
    while l < n and r < m:
        if (b[r] <= a[l] + k and b[r] >= a[l] - k ):
            count += 1
            l += 1
            r += 1
        else:
            if a[l] < b[r]:
                l += 1
            else:
                r += 1

    return count
    
print(distribution(n, m, k, a, b))

# import heapq
# heapq.heapify(A)
# heapq.heapify(B)
# ans = 0
# while len(B) > 0 and len(A) > 0:
#     currA = heapq.heappop(A)
#     currB = heapq.heappop(B)
#     if abs(currA - currB) <= k:
#         ans += 1
#     else:
#         if currA < currB:
#             heapq.heappush(B, currB)
#         else:
#             heapq.heappush(A, currA)

# print(ans)