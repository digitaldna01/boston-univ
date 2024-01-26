#
# Name: CS 111 Staff
#
# lab3.py
#

def num_consonants(s):
    """ returns the number of consonants in s
        parameter: s is a string of lower-case letters
    """
    print("beginning run for", s)
    if s == '':
        print('end of base case:',0,'for', s)
        return 0
    else:
        num_in_rest = num_consonants(s[1:])
        if s[0] not in 'aeiou':
            print('end of consonant case:', num_in_rest,'for', s)
            return num_in_rest + 1
        else:
            print('end of vowel case:',num_in_rest + 1,'for', s)
            return num_in_rest 
