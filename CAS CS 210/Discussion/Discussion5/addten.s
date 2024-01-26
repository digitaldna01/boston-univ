	.intel_syntax noprefix
	.section .data
x:	.quad 586
y:	.quad 478
z:	.quad 821
t:	.quad 578
result:	 .quad

	.section .text
	.global _start
_start:
	mov rax, 599
	mov rbx, QWORD PTR [x]
	add rax, rbx
	add rax, 122
	mov rbx, QWORD PTR [y]
	add rax, rbx
	add rax, 58
	mov rbx, QWORD PTR [z]
	add rax, rbx
	add rax, 926
	mov rbx, QWORD PTR [t]
	add rax, rbx
	add rax, 55
	mov rbx, 72
	add rax, rbx
	mov QWORD PTR [result], rax

	/* Call OS EXIT system call */
	mov rax, 60
	mov rdi, QWORD PTR [result]
	syscall
