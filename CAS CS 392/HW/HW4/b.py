from itertools import permutations

n = int(input())

lucky_num = [4, 7]

def find_num(digit, n):
    mininum = float('inf')
    
    signal = [4] * (digit // 2) + [7] * (digit // 2)

    for subset in set(permutations(signal)):
        num = int("".join(map(str, subset)))
        if num >= n:
            mininum = min(mininum, num)
    
    if mininum == float('inf'):
        return find_num(digit + 2, n)
    
    return mininum

def lucky(n):
    digit_count = len(str(n)) if len(str(n)) % 2 == 0 else len(str(n)) + 1
    return(find_num(digit_count, n))
    

print(lucky(n))