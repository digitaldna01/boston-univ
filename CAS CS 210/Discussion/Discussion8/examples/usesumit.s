	.intel_syntax noprefix
	.section .text
	.global _start
_start:
	call sumit

	# save result to stack
	push rax
	# write result to standard out
	mov rax, 1
	mov rdi, 1
	mov rsi, rsp
	mov rdx, 8
	syscall

	# exit with return 0 to OS as exit status
	mov rax, 60
	mov rdi, 0
	syscall
	
	.section .data
	.global XARRAY
XARRAY:	.quad 1, 2, 3, 4, 5, -15
	.quad 1, 1, 1, 1
	
	.section .note.GNU-stack,"",@progbits

	
