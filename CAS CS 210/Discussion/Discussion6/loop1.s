	.intel_syntax noprefix

	.section .data
positive_count:
	.quad 0
negative_count:
	.quad 0
array:
	.quad 1 
	.quad 2
	.quad -4
	.quad 5
	.quad 7
	.quad -13
	
	.section .text
	.global _start
_start:
	xor rdi, rdi
loop_start:
	cmp rdi, 6
	je loop_done
	cmp QWORD PTR [array+rdi*8], 0              
	jl is_neg
	inc QWORD PTR [positive_count]
	jmp done_cond
is_neg:
	inc QWORD PTR [negative_count]
done_cond:
	inc rdi
	jmp loop_start
loop_done:	
	mov rax, 60
	mov rdi, 0
	syscall
