	.intel_syntax noprefix

	.section .data
mystr:	.asciz "Hello World\n"

	.section .text
	.global _start
_start:
	mov rax, 1
	mov rdi, 1
	mov rsi, OFFSET mystr
	# note length does not include the 0 to
	# ensure we only send valid ascii data
	mov rdx, 12
		# syscall instruction over writes, clobbers, rcx
	# (see intel manuals for details)
	syscall             

	mov rax, 60
	mov rdi, 0
	syscall
