t = int(input())

while t:
    t-=1
    n,a,b,c = map(int,input().split())
    d = n//(a+b+c)
    if d*a+d*b+d*c >= n:
        print(3*d)
    elif d*a+d*b+d*c+a >=n:
        print(3*d+1)
    else:
        print(3*d+2)