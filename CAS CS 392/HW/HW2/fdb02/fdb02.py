n,m = map(int,input().split())
a = list(map(int,input().split()))
p = [0]*(n+1)
q = [0]*(n+1)
for i in range(1,len(a)):
    if a[i] < a[i-1]:
        p[i] = a[i-1] - a[i] 
    if a[i] > a[i-1]:
        q[i] = a[i] - a[i-1] 
        
for i in range(1,len(a)):
    p[i] += p[i-1]
for i in range(1, len(a)):
    q[i] += q[i-1] 
    

while m:
    m-=1
    s,t = map(int,input().split())
    if s < t:
        print(p[t-1] - p[s-1])
    else:
        print(q[s-1] - q[t-1])