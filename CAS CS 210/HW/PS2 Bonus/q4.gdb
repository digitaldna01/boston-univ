# q4 function count the number of bits that are set to 1 in the value of the rax register and place the result in rbx

# change empty file _start to popcnt rbx, rax
# opcode for this instruction is 0xf3, 0x48, 0x0f, 0xb8, 0xd8
# set first memory address of _start to 0xf3
# set second memory address of _start to 0x48
# set third memory addesss of _start to 0x0f
# set forth memory address of _start to 0xb8
# set fifth memory address of _start to 0xd8

define q4
       set {char}(((char *)&_start)) = 0xf3
       set {char}(((char *)&_start+1)) = 0x48
       set {char}(((char *)&_start+2)) = 0x0f
       set {char}(((char *)&_start+3)) = 0xb8
       set {char}(((char *)&_start+4)) = 0xd8
end