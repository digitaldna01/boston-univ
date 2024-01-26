	.intel_syntax noprefix

	.section .data
positive_count:
	.quad 0
negative_count:
	.quad 0
x:
	.quad 100

	.section .text
	.global _start
_start:
	mov rax, QWORD PTR [x]
	cmp rax, 0
	jl is_neg
	mov rbx, QWORD PTR [positive_count]
	inc rbx
	mov QWORD PTR [positive_count], rbx
	jmp done_cond
is_neg:
	mov rcx, QWORD PTR [negative_count]
	inc rcx
	mov QWORD PTR [negative_count], rcx
done_cond:

	mov rax, 60
	mov rdi, 0
	syscall
