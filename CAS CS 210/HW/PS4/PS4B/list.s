	.intel_syntax noprefix

	.section .text
	# Tell linker that LIST_FRAG symbols can be referenced on other files
	.global LIST_FRAG
	# Code to execute two command based on the list address value
	# Run second argument with the given frag
LIST_FRAG:				
	movzx rdi, BYTE PTR [rbx + 1]		# Copy second commend to rdx
	add rbx, 8				# Add rbx 8 bytes
	push rbx				# Push rbx address
	mov rbx, QWORD PTR [rbx]		# mov rbx from address value to the actual value

find_list_command_start:
	cmp rbx, 0				# Check if the loop is done
	je list_command_done
	push rdi
	cmp rdi, '&'				# Check if the second command is 'and'
	je EXECUTE_LIST_AND			# Execute and routine
	cmp rdi, '|'				# Check if the second command is 'or'
	je EXECUTE_LIST_OR			# Execute or routine
	cmp rdi, 'S'				# Check if the second command is 'sub'
	je EXECUTE_LIST_SUB			# Execute sub routine
	cmp rdi, 'U'				# Check if the second command is 'upper'
	je EXECUTE_LIST_UPPER			# Execute upper routine
	
	jmp find_list_command_start
	
EXECUTE_LIST_AND:				# Execute and routine
	call AND_FRAG
	pop rdi
	mov rbx, QWORD PTR [rbx]
	jmp find_list_command_start

EXECUTE_LIST_OR:				# Execute or routine
	call OR_FRAG
	pop rdi
	mov rbx, QWORD PTR [rbx]
	jmp find_list_command_start

EXECUTE_LIST_SUB:				# Execute sub routine
	call SUB_FRAG
	pop rdi
	mov rbx, QWORD PTR [rbx]
	jmp find_list_command_start

EXECUTE_LIST_UPPER:				# Execute upper routine
	call UPPER_FRAG
	pop rdi
	mov rbx, QWORD PTR [rbx]
	jmp find_list_command_start

list_command_done:
	pop rbx					# Pop the original rbx
	add rbx, 8				# Add rbx 8 bytes to the next bytes
	ret					# Return the call from where it is called from
