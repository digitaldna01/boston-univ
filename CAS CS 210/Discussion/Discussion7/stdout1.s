	.intel_syntax noprefix

	.section .data
x:	.quad 0xdeadbeeffeedface

	.section .text
	.global _start
_start:
	mov rax, 1
	mov rdi, 1
	mov rsi, OFFSET x
	mov rdx, 8
	
	# syscall instruction over writes, clobbers, rcx
	# (see intel manuals for details)
	syscall             

	mov rax, 60
	mov rdi, 0
	syscall
