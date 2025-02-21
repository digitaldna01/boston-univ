time = list(map(int, input().split()))
n, k = time[0], time[1]
theorem = list(map(int, input().split()))
sleep = list(map(int, input().split()))
sleeping_theorem = [None] * (n+1)
sleeping_theorem[0] = 0
sleeping_start = -1
max = 0
output = 0
# Get the current n of theorem 
for i in range(n):
    if (sleep[i] != 0):
        output += theorem[i]
        sleeping_theorem[i+1] = sleeping_theorem[i]
    else:
        if (sleeping_start == -1):
            sleeping_start = i
        
        sleeping_theorem[i+1] = sleeping_theorem[i] + theorem[i]

if (sleeping_start == -1):
    print(output)
else:
    for j in range(n-sleeping_start-k+1):

        if (sleeping_theorem[sleeping_start + j + k] - sleeping_theorem[j+ sleeping_start] > max):
            max = (sleeping_theorem[sleeping_start + j + k] - sleeping_theorem[j+ sleeping_start])

    print(max + output)