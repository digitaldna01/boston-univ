a = list(map(int,input().split()))
n, free = a[0], a[1]
t = list(map(int, input().split()))
j = 0
max = 0
time = 0
for i in range(n):
    time = time + t[i]
    while time > free:
        time = time - t[j]
        j += 1
    if(i - j + 1 > max):
        max = i - j + 1
print(max)  
# while j > -1:
#     if(time + t[j] <= free):
#         time = time + t[j]
#         j -= 1
#     else:
#         if(i - j > max):
#             max = i - j
#         i -= 1
#         j = i
#         time = 0

# print(max)
# i = 0
# j = 0
# max = 0
# time = 0
# count = 0
# while i < n :
#     if(j < n and (time + t[j]) <= free):
#         time += t[j]
#         j += 1
#         count += 1
#     else:
#         i += 1
#         j = i
#         time = 0
#         if(count > max):
#             max = count
#         count = 0
# print(max)
