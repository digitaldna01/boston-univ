# Read line by line from hps.in
with open('hps.in', 'r') as file:
    list = []
    for line in file:
        # print every line
        list.append(line.strip())
    n = int(list[0])
    cow = list[1:]
    
    h_prefix = [0] * (n+1)
    s_prefix = [0] * (n+1)
    p_prefix = [0] * (n+1)
    
    for i in range(n):
        if cow[i] == "P":
            p_prefix[i+1] += 1
        elif cow[i] == "S":
            s_prefix[i+1] += 1
        else:
            h_prefix[i+1] += 1
        
        h_prefix[i+1] += h_prefix[i]
        s_prefix[i+1] += s_prefix[i]
        p_prefix[i+1] += p_prefix[i]
        
    # print("H prefix : ", h_prefix)
    # print("P prefix : ", p_prefix)
    # print("S prefix : ", s_prefix)
    
    max_value = 0
    if (max(h_prefix) > max(p_prefix)):
        if(max(h_prefix) > max(s_prefix)):
            max_value = max(h_prefix)
            index = h_prefix.index(max_value)
            s_value = s_prefix[n] - s_prefix[index]
            p_value = p_prefix[n] - p_prefix[index]
            
            if (s_value > p_value):
                max_value += s_value
            else:
                max_value += p_value
        else:
            max_value = max(s_prefix)
            index = s_prefix.index(max_value)
            h_value = h_prefix[n] - h_prefix[index]
            p_value = p_prefix[n] - p_prefix[index]
            
            if (h_value > p_value):
                max_value += h_value
            else:
                max_value += p_value
    else:
        if (max(p_prefix) > max(s_prefix)):
            max_value = max(p_prefix)
            index = p_prefix.index(max_value)
            s_value = s_prefix[n] - s_prefix[index]
            h_value = h_prefix[n] - h_prefix[index]
            
            if (s_value > h_value):
                max_value += s_value
            else:
                max_value += h_value
        else:
            max_value = max(s_prefix)
            index = s_prefix.index(max_value)
            p_value = p_prefix[n] - p_prefix[index]
            h_value = h_prefix[n] - h_prefix[index]
            
            if (p_value > h_value):
                max_value += p_value
            else:
                max_value += h_value
                
    with open("hps.out", "w") as file:
        file.write(str(max_value))
