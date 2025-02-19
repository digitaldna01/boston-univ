a,b,c = list(map(int, input().split()))

def s(n):
    sum = 0
    for d in str(n):
        sum += int(d)
    return sum

def equation(a, b, c):
    results = []
    max_b = 10000
    
    for sum in range(1, max_b + 1):
        x = b * (sum ** a) + c
        
        if (0 < x < 10**9 and s(x) == sum) :
            results.append(x)
    
    print(len(results))
    if len(results) != 0 or len(results) < 10**9:
        print(*results)
        

equation(a, b, c)

# def find_solutions(a, b, c):
#     solutions = []
#     max_Sum = 10000

#     for sum in range(1, max_Sum+1):
#       x = b * (sum ** a) + c

#       if 0 < x < 10**9 and sum_of_digits(x) == sum :
#         solutions.append(x)

#     print(len(solutions))
#     if(len(solutions) != 0 or len(solutions) < 10**9):  
#       print(*solutions)



# def sum_of_digits(n):
#     return sum(int(d) for d in str(n))