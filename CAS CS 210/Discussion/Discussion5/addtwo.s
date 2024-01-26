	.intel_syntax noprefix
	.section .data
x:	.quad 2
result:	 .quad

	.section .text
	.global _start
_start:
	mov rax, 1
	mov rbx, QWORD PTR [x]
	add rax, rbx
	mov QWORD PTR [result], rax

	/* Call OS EXIT system call */
	mov rax, 60
	mov rdi, QWORD PTR [result]
	syscall
