	.intel_syntax noprefix

	.section .text
	.global _start
_start:
	mov rax, OFFSET flowers
	mov rbx, 13
	xor rdi, rdi
	xor rcx, rcx
	
loop_head:
	mov rdx, QWORD PTR [rax]
	cmp BYTE PTR [rdx], 'c
	jne loop_next
	mov rsi, QWORD PTR [rax + 8]
	imul rsi, QWORD PTR [rax + 16]
	push rsi     # mywritestr expects pointer to string in rsi
	mov rsi, rdx
	call mywritestr
	pop rsi
	add rcx, rsi
	
loop_next:
	add rax, 24
	inc rdi
	cmp rdi, rbx
	jl loop_head
	
	mov rax, 60
	mov rdi, rcx
	syscall

	# To use this code correctly:
	#  call with pointer to zero temrinate string in rsi
	# inputs: rsi = & string
	# outputs: none
	# all registers used are restored to their orginal values
mywritestr:
	push rax
	push rdi
	push rdx
	push rcx     # clobbered by system call instruction
	push r11     # clobbered by system call instruction
	
	xor rdx,rdx
loop_strlen:
	cmp BYTE PTR [rsi + rdx],0
	je loop_strlen_done
	inc rdx
	jmp loop_strlen
loop_strlen_done:

	mov rax, 1
	mov rdi, 1
	# syscall instruction over writes, clobbers, rcx
	# (see intel manuals for details)
	syscall             

	mov rax, 1
	mov rdi, 1
	push rsi
	mov rsi, OFFSET newline
	mov rdx, 1
	# syscall instruction over writes, clobbers, rcx
	# (see intel manuals for details)
	syscall             
	
	pop rsi
	pop r11
	pop rcx
	pop rdx
	pop rdi
	pop rax

	ret
	
	.section .data
newline:	.byte '\n
	
flowers:
	.quad lilystr
	.quad 5
	.quad 3
	.quad irisstr
	.quad 7
	.quad 3
	.quad buttercupstr
	.quad 4
	.quad 5
	.quad wildrosestr
	.quad 2
	.quad 5
	.quad larkspurstr
	.quad 9
	.quad 5
	.quad columbinestr
	.quad 2
	.quad 5
	.quad delphiniumsstr
	.quad 3
	.quad 8
	.quad ragwortstr
	.quad 4
	.quad 13
	.quad cinerariastr
	.quad 1
	.quad 13
	.quad asterstr
	.quad 2
	.quad 21
	.quad chicorystr
	.quad 1
	.quad 21
	.quad plantainstr
	.quad 8
	.quad 34
	.quad pytethrumstr
	.quad 10
	.quad 34

names:
lilystr:	.asciz "lily"
irisstr:	.asciz "iris"
buttercupstr:	.asciz "buttercup"
wildrosestr:	.asciz "wild rose"
larkspurstr:	.asciz "larkspur"
columbinestr:	.asciz "columbine"
delphiniumsstr:	.asciz "delphiniums"
ragwortstr:	.asciz "ragwort"
cinerariastr:	.asciz "cineraria"
asterstr:	.asciz "aster"
chicorystr:	.asciz "chicory"
plantainstr:	.asciz "plantain"
pytethrumstr:	.asciz "pytethrum"
