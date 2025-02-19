from itertools import combinations

flag = True

def generate_subsets(n, input_list):
    difference = n - 6
    return list(combinations(input_list, difference))[::-1]

while (1):
    array = list(map(int, input().split()))
    n, arr = array[0], array[1:]
    
    # terminate if the input is 0
    if n == 0:
        break
    if not flag:
        print()
    flag = False
    
    subsets = generate_subsets(n, arr)
    results = []
    for subset in subsets:
        combin = " ".join(str(num) for num in arr if num not in subset)
        results.append(combin)
    print("\n".join(results))