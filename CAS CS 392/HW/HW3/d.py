from collections import defaultdict
import math

n = int(input())

gear_teeth = defaultdict(list)

for _ in range(n):
    s, c = map(int, input().split())
    gear_teeth[s].append(c)
    
log_max_speed = 0.0

for gears in gear_teeth.values():
    gears.sort() 
    i, j = 0, len(gears) - 1
    while i < j:
        log_max_speed += math.log(gears[j] / gears[i])
        i += 1
        j -= 1
print(log_max_speed)  
