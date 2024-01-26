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
	cmp QWORD PTR [x], 0
	jl is_neg
	inc QWORD PTR [positive_count]
	jmp done_cond
is_neg:
	inc QWORD PTR [negative_count]
done_cond:

	mov rax, 60
	mov rdi, 0
	syscall
