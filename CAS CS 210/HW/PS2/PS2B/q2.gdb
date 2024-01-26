# q2 function computes the bitwise logical and of the first operand and second operand
# change empty file _start to test rax, rbx
# opcode for this instruction is 0x48, 0x85, 0xd8, 0x00, 0x00
# set first memory address of _start to 0x48
# set second memory address of _start to 0x85
# set third memory addesss of _start to 0xd8
# set forth memory address of _start to 0x00
# set fifth memory address of _start to 0x00

define q2
       set {char}(((char *)&_start)) = 0x48
       set {char}(((char *)&_start+1)) = 0x85
       set {char}(((char *)&_start+2)) = 0xd8
       set {char}(((char *)&_start+3)) = 0x00
       set {char}(((char *)&_start+4)) = 0x00
end