m, s = map(int, input().split())

def small_large(m ,s):
    if s == 0:
        return("0 0" if m ==1 else "-1 -1")
    if s > 9 * m :
        return("-1 -1")
    
    s_large, s_small = s, s
    l_list = []

    for i in range(m):
        digit = min(9, s_large)
        l_list.append(str(digit))
        s_large -= digit

    s_list = ['0'] * m

    for i in range(m -1, 0, -1):
        digit = min(9, s_small -1)
        s_list[i] = str(digit)
        s_small -= digit

    s_list[0] = str(s_small)

    return("".join(s_list) + " " + "".join(l_list))

print(small_large(m, s))