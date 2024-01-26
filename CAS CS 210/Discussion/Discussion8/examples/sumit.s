	.intel_syntax noprefix
	.section .text
	.global sumit
	# code to sum data at XARRAY
	# hard coded length 10
sumit:	                      
	xor  rax, rax            # rax -> sum : sum = 0
	xor  rdi, rdi            # rdi -> i : i = 0
loop_start:
	cmp  rdi, 10                           # i - 10
	je   loop_done                         # if equal done
	add  rax, QWORD PTR [XARRAY + rdi * 8] # sum += XARRAY[i]
	inc  rdi                               # i=i+1
	jmp  loop_start                       
loop_done:
        ret	
	
	.section .note.GNU-stack,"",@progbits
