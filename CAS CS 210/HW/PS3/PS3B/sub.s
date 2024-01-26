	.intel_syntax noprefix

	.section .data
	# tell linker that SUB_FRAG, SUB_POSITIVE, SUB_NEGATIVE symbols can be referenced in other files
	.global SUB_NEGATIVE
	.global SUB_POSITIVE
SUB_NEGATIVE:
	.quad 0x0
SUB_POSITIVE:
	.quad 0x0
	
	.section .text
	.global SUB_FRAG
	# code to subtract rax as y from rbx as x
	# if y is positive then add y into an 8 byte value stored at a symbol SUB_POSITIVE
	# if y is negatice then subtract y from an 8 byte value stored at a symbol SUB_NEGATICE
	# Update rbx to rbx + 8 for next input array of rbx
SUB_FRAG:
	xor rdi, rdi
	sub rax, QWORD PTR [rbx]		# subtract y from x
	cmp QWORD PTR [rbx], 0			# compare y with 0
	jl is_neg
	mov rdi, QWORD PTR [rbx] 		# if y is positive, add y into SUB_POSITIVE
	add QWORD PTR [SUB_POSITIVE], rdi
	jmp done
is_neg:						# if y is negative operate subtract y from SUB_NEGATIVE
	mov rdi, QWORD PTR [rbx]		# copy rbx value to rdi
	sub QWORD PTR [SUB_NEGATIVE], rdi	#sub tract rdi value from SUB_NEGATIVE
	jmp done
done:	
	add rbx, 8				# update rbx to next 8 bytes address
	int3					# give up and trap to the debugger
	
