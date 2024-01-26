	.intel_syntax noprefix

	.section .data
x:
	.quad 2
result:
	.quad
	
	.section .text
	.global _start
_start:
	mov rax, 1
	mov rbx, QWORD PTR [x]   
	add rax, rbx

	mov QWORD PTR [result], rax
	
	
	/* Call OS EXIT system call */
	mov rax, 60    # move exit system call number 60 into rax
	mov rdi, QWORD PTR [result] # move exit status code into rdi
	syscall      # call OS kernel (process will terminate)
