#
# Lab 5, Task 0
#

def bitwise_or(b1, b2):
    """ computes and returns the bitwise OR of binary numbers b1 and b2
        inputs: b1 and b2 are strings that represent binary numbers
    """
    if b1 == '' and b2 == '':
        return ''
    elif b1 == '':
        return b2
    elif b2 == '':
        return b1
    else:
        # implement the recursive case here
        rest = bitwise_or(b1[:-1],b2[:-1])
        if b1[-1] == '1' or b2[-1] == '1':
            return rest + '1'
        else: 
            return rest + '0'
           
def test():
    #test functions above
    print('bitwise_or("","") return', bitwise_or('',''))
    print('bitwise_or("101","") return', bitwise_or('101',''))
    print('bitwise_or("","11010") return', bitwise_or('','11010'))
    print('bitwise_or("10100","00101") return', bitwise_or('10100','00101'))
    print('bitwise_or("10101010","11000") return', bitwise_or('10101010','11000'))