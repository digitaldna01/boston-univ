	.intel_syntax noprefix
	.data
x:	 .quad 142
y:	 .quad 4200
sum:	 .quad
	.text
	.global _start
_start:
	mov rax, QWORD PTR x # mov takes two operands and moves data from the second perand to the firt operand 
	add rax, QWORD PTR y # add the value of the second operand to the first operand and stores the result in the first operand
	mov QWORD PTR sum, rax
	int3
