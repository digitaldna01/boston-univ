	.intel_syntax noprefix

	.section .text
	.global ARRAYSUB_FRAG
	# Code to loop throught each value in the array and subtract them from rax
	# SUB_POSITIVE and SUB_NEGATIVE values are also updates depends on each array values
ARRAYSUB_FRAG:
	xor rdi, rdi				# Assign rdi = 0
	xor rcx, rcx				# Assign rcx = 0
	mov rdx, QWORD PTR [rbx + 8]		# Assign rdx the int array

loop_arraysub_start:
	cmp rdi, QWORD PTR [rbx]
	je loop_arraysub_done			# check if the array is over
	mov rcx, QWORD PTR [rdx + rdi * 8]	# Copy array value to rcx register
	sub rax, rcx
	cmp rcx, 0
	jl arraysub_is_neg			# Check if the array value is negative
	add QWORD PTR [SUB_POSITIVE], rcx	# If the array value is positive then add array value to SUB_POSITIVE
	inc rdi
	jmp loop_arraysub_start		# Return back to the next array

arraysub_is_neg:			# if the array value is negative then subtact array value from SUB_NEGATIVE
	sub QWORD PTR [SUB_NEGATIVE], rcx
	inc rdi
	jmp loop_arraysub_start		# Return back to the next array
	
loop_arraysub_done:
	add rbx, 16			# Update rbx to next 16 bytes address
	ret				# Return back to where they get called from
