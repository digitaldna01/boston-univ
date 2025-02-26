n, x = map(int, input().split())
array = list(map(int, input().split()))

pair_arr = ((value, index) for index, value in enumerate(array))
sorted_arr = sorted(pair_arr)

flag = False
target = {}

l, r = 0, n - 1

while l < r:
    sum = sorted_arr[l][0] + sorted_arr[r][0]
    if sum == x:
        print(sorted_arr[l][1] + 1, sorted_arr[r][1] + 1)
        flag = True
        break
    else:
        if sum < x:
            l += 1
        else:
            r += 1

if not flag:
    print("IMPOSSIBLE")

# index_1, index_2 = -1, -1
# for i in range(n):
#     targetValue = (x - array[i])
#     if targetValue in target:
#         print(target[targetValue] + 1, i + 1)
#         flag = True
#         break

#     target[array[i]] = i


# arrayCopy = array.copy()
# arrayCopy.append(x)
# arrayCopy.sort()
# end = arrayCopy.index(x) # last digit to check 
# arrayCopy = arrayCopy[:end]
# index_1, index_2 = -1, -1

# for i in range(end):
#     if (x - arrayCopy[i]) in arrayCopy:
#         index_1 = array.index(arrayCopy[i])
#         index_2 = array.index(x-arrayCopy[i])

# if index_1 > 0:
#     print(index_1+1, index_2+1)
# else:
#     print("IMPOSSIBLE")


