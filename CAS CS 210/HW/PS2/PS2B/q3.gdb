# from empty file change the memory byte of _start to 0x48, 0x01, 0xd8, 0x48, 0x89, 0xc2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
# similar to q2 change byte from _start memort with set command 
define q3
       set {char}(((char *)&_start)) = 0x48
       set {char}(((char *)&_start+1)) = 0x01
       set {char}(((char *)&_start+2)) = 0xd8
       set {char}(((char *)&_start+3)) = 0x48
       set {char}(((char *)&_start+4)) = 0x89
       set {char}(((char *)&_start+5)) = 0xc2
       set {char}(((char *)&_start+6)) = 0x00
       set {char}(((char *)&_start+7)) = 0x00
       set {char}(((char *)&_start+8)) = 0x00
       set {char}(((char *)&_start+9)) = 0x00
       set {char}(((char *)&_start+10)) = 0x00
       set {char}(((char *)&_start+11)) = 0x00
end