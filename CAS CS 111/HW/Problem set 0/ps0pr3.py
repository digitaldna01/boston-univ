#
# ps0pr3.py - Problem Set 0, Problem 3
#
# Computes the integers 0 through 4 using exactly four fours.
#
# name: Jae Hong Lee
# email: jhonglee@bu.edu
#

zero = 4 + 4 - 4 - 4
one = (4 + 4)//(4 + 4)
two = 4//4 + 4//4
three = (4+4+4) // 4
four = 4 * (4 - 4) + 4
# Put your definitions of the remaining variables below.






# The code below tests the values of your expressions. DO NOT MODIFY IT!
if __name__ == '__main__':    
    for x in ['zero', 'one', 'two', 'three', 'four']:
        if x in dir():
            print(x, '=', eval(x))
