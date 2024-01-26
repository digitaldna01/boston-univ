	.intel_syntax noprefix

	.section .data
c:	.quad 0
mystr:
	.asciz "WalDo wAlDO WALDO"

	.section .text
	.global _start
_start:
	xor rdi, rdi
	xor rcx, rcx
	mov rbx, OFFSET [mystr]
loop_start:
	mov al, BYTE PTR [rbx + rdi * 1]
	cmp al, 0
	je loop_end
	cmp al, 'a
	jb loop_next
	cmp al, 'z
	ja loop_next
	inc rcx
loop_next:
	inc rdi
	jmp loop_start
loop_end:
	mov QWORD PTR [c], rcx
	
	mov rax, 60
	mov rdi, 0
	syscall
