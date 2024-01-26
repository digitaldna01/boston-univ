	.intel_syntax noprefix

	.section .text
	# Tell linker that ARRAY_FRAG symbols can be referenced on other files
	.global ARRAY_FRAG
	# Code to execute two command based on the list in array
	# Run second argument with given frags 
ARRAY_FRAG:
	xor rdi, rdi				# Assign rdi = 0
	movzx rdx, BYTE PTR [rbx + 1]		# Copy second command to rdx
	add rbx, 8				# move rbx to the next 8 bytes
	mov rcx, QWORD PTR [rbx]		# Copy number of integer arrays to rcx
	add rbx, 8
	push rbx				# Move rbx to the next 8 bytes
	mov rbx, QWORD PTR [rbx]		# Copy array value to rbx

find_command_start:
	cmp rdi, rcx				# Check loop is done
	je loop_done				# finish loop 
	push rdi				# Push rdi before run other frag
	push rdx				# Push rdx before run other frag
	push rcx				# Push rcx before run other frag
	cmp rdx, '&'				# Check if the second command is 'and'
	je EXECUTE_ARRAY_AND			# Execute and routine
	cmp rdx, '|'				# Check if the second command is 'or'
	je EXECUTE_ARRAY_OR			# Execute or routine
	cmp rdx, 'S'				# Check if the second command is 'sub'
	je EXECUTE_ARRAY_SUB			# Execute sub routine
	cmp rdx, 'U'				# Check if the second command is 'upper'
	je EXECUTE_ARRAY_UPPER			# Execute upper routine
	jmp find_command_start			

EXECUTE_ARRAY_AND:				# Execute and routine
	call AND_FRAG		
	pop rcx
	pop rdx
	pop rdi
	inc rdi					# Increase the index
	jmp find_command_start	
	
EXECUTE_ARRAY_OR:				# Execute or routine
	call OR_FRAG
	pop rcx
	pop rdx
	pop rdi
	inc rdi					# Increase the index
	jmp find_command_start
	
EXECUTE_ARRAY_SUB:				# Execute sub routine
	call SUB_FRAG
	pop rcx
	pop rdx
	pop rdi
	inc rdi					# Increase the index
	jmp find_command_start
	
EXECUTE_ARRAY_UPPER:				# Execute upper routine
	call UPPER_FRAG
	pop rcx
	pop rdx
	pop rdi
	inc rdi					# Increase the index
	jmp find_command_start

loop_done:
	pop rbx					# Pop the original rbx
	add rbx, 8				# Add rbx 8 bytes to the next bytes
	ret					# Return the call from where it is called from
	
