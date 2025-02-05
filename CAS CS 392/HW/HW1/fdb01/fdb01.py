t = int(input())

while t:
    t-=1
    n,a,b,c = map(int,input().split())
    d = n//(a+b+c)
    if d*a+d*b+d*c >= n:
        print(3*d)
    elif d*a+d*b+d*c+a >=n:
        print(3*d+1)
    elif d*a+d*b+d*c+a+b >=n:
        print(3*d+2)
    else:
        print(3*d+3)
        
# while t:
#     t-=1
#     n,a,b,c = map(int,input().split())
#     d = n//(a+b+c)
#     if d*a+d*b+d*c >= n:
#         print(3*d)
#     elif d*a+d*b+d*c+a >=n:
#         print(3*d+1)
#     else:
#         print(3*d+2)