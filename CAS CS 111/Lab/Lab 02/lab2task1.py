#
# Name: 
#
# lab2task1.py
#

num = [8, 6, 7, 5, 3, 0, 9]
info = [4, 1, 1]

# Expression for the list [8, 7, 3, 9].
list1 = num[::2]
print(list1)

# Expression for the list [9, 1, 1].
list2 = num[-1:] + info[1:]
print(list2)

# Expression for the list [4, 1, 1, 6, 5, 0].
list3 = info + num[1:6:2]
print(list3)
