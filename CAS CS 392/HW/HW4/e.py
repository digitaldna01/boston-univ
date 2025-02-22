from itertools import product

def lock(n, angle):
    ans = "NO"
    # possible_array = []
    possible_array = list(product([1, -1], repeat=n)) 
    for subset in possible_array:
        value = 0
        for j in range(n):
            value += subset[j] * angle[j]
        if value % 360 == 0:
            ans = "YES"
    
    return ans

n = int(input())
angle = [None] * n
for i in range(n):
    angle[i] = int(input())

print(lock(n, angle))
