# from empty file change the memory byte of _start to 0xf3, 0x48, 0x0f, 0xb8, 0xd8, 0x48, 0x89, 0x1d, 0x00, 0x00, 0x00, 0x00
# similar to q3 change byte from _start memort with set command
define q5
       set {char}(((char *)&_start)) = 0xf3
       set {char}(((char *)&_start+1)) = 0x48
       set {char}(((char *)&_start+2)) = 0x0f
       set {char}(((char *)&_start+3)) = 0xb8
       set {char}(((char *)&_start+4)) = 0xd8
       set {char}(((char *)&_start+5)) = 0x48
       set {char}(((char *)&_start+6)) = 0x89
       set {char}(((char *)&_start+7)) = 0x1d
       set {char}(((char *)&_start+8)) = 0x00
       set {char}(((char *)&_start+9)) = 0x00
       set {char}(((char *)&_start+10)) = 0x00
       set {char}(((char *)&_start+11)) = 0x00
end