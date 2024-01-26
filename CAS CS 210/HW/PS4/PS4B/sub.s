	.intel_syntax noprefix

	.section .data
	# Tell linker that SUB_FRAG, SUB_POSITIVE, SUB_NEGATIVE symbols can be referenced in other files
	.global SUB_POSITIVE
	.global SUB_NEGATIVE
SUB_POSITIVE:
	.quad 0x0
SUB_NEGATIVE:
	.quad 0x0

	.section .text
	.global SUB_FRAG
	# Code to subtract rax as y from rbx as x
	# If y is positive then add y into 8 bytes value stored at a symbol SUB_POSITIVE
	# If y is negative then subtract y from 8 bytes value stored at a symbol SUB_NEGATIVE
	# Update rbx to rbx + 8 for next input array of rbx
SUB_FRAG:
	xor rdi, rdi
	sub rax, QWORD PTR [rbx]		# Subtract y from x
	cmp QWORD PTR [rbx], 0			# Compare y with 0
	jl is_neg
	mov rdi, QWORD PTR [rbx]		# if y is positive, add y into SUB_POSITIVE
	add QWORD PTR [SUB_POSITIVE], rdi
	jmp done

is_neg:						# If y is negative, subtract y from SUB_NEGATIVE
	mov rdi, QWORD PTR [rbx]		# Copy rbx value to rdi
	sub QWORD PTR [SUB_NEGATIVE], rdi	# Subtract rdi value from SUB_NEGATIVE
	jmp done

done:
	add rbx, 8				# Update rbx to next 8 bytes address
	ret					# Return back to where they get called from
	
	
