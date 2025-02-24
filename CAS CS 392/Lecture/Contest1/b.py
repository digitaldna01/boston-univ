from itertools import permutations

s = map(str, input())

list = list(set(permutations(s)))
a_list = []
for i in list:
    a_list.append("".join(i))

l = len(a_list)
print(l)
for item in sorted(a_list):
    print(item)
