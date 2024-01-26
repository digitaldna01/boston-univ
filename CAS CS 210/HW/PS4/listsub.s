	.intel_syntax noprefix
	
	.section .text
	.global LISTSUB_FRAG
	# Code to loop through each values in the list and subtract them from rax
	# SUB_POSITIVE and SUB_NEGATIVE values are also updated depends on each list values
LISTSUB_FRAG:
	xor rcx, rcx				# Assigne rcx = 0
	mov rdx, QWORD PTR [rbx]		# assign rdx the list head address

loop_listsub_start:
	cmp rdx, 0				# Check if the list is over by checking address is 0
	je loop_listsub_done			# Finish loop of the list is over 
	mov rcx, QWORD PTR [rdx]
	sub rax, rcx				# Subtract list value from rax value
	cmp rcx, 0				# Check if the list value is negative
	jl listsub_is_neg
	add QWORD PTR [SUB_POSITIVE], rcx	# If the list value is positive then add list value to SUB_POSITIVE
	mov rdx, QWORD PTR [rdx + 8]
	jmp loop_listsub_start			# Return back to the next list
	
listsub_is_neg:
	sub QWORD PTR [SUB_NEGATIVE], rcx	# If the list value is negative then subtract list value from SUB_NEGATIVE
	mov rdx, QWORD PTR [rdx + 8]
	jmp loop_listsub_start			# Return back to the next list

loop_listsub_done:
	add rbx, 8				# Update rbx to next 8 bytes address 
	ret					# Return back to where the y get called from
