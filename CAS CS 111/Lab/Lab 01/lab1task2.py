
\
#
# lab1task2.py
#
# name: CS 111 course staff
# email: cs111-staff@cs.bu.edu
#

course = 111
print('congratulations on taking CS', course)

#1) i is added to the course = 111, so now course is stored as 112
course = course + 1
print('maybe you will take CS', course, 'next semester')
print()

days = 40
print('the first midterm is in fewer than', days, 'days')

weeks = days // 7
print('that is approximately', weeks, 'weeks')
#2. A) the difference between weeks and 'weeks' is that the weeks is int which is the number stored in variable 
# and 'weeks' is string of characrters

#2. B) since // is integer division, so it shows 5 instead of float 5.714857
# we use / for regular division

#2. C) we use regular division / than integer division //

print()
print('Go Terriers!')
print('pi is approximately', (22 / 7))
#4. the code does not run because of the error on ('go terriers!")