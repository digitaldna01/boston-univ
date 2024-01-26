	.intel_syntax noprefix
	.text
	.global _start
_start:
	# zero out rax
	xor rax, rax
	# setup rbx to point to the start of the commands
	mov rbx, OFFSET [CALC_DATA_BEGIN]

	# just exit
	mov rax, 60
	mov rdi, 0
	syscall
