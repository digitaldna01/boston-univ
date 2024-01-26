	.intel_syntax noprefix
	# Simple driver that iterates over the command array
	.section .data
final_value:				# Variable to store final value
	.quad 0x0
	
	.section .text
	#  tell linker that _start symbols can be referenced in ohter files
	.global _start
_start:
	xor rax, rax 				# initialize RAX register to zero
	mov QWORD PTR [SUB_POSITIVE], 0			# Initialize SUB_POSITIVE memory value to 0
	mov QWORD PTR [SUB_NEGATIVE], 0			# Initialize SUB_NEGATIVE memory value to 0
	mov rbx, OFFSET [CALC_DATA_BEGIN] 	# initialize RBX register ti the address of CALC_DATA_BEGIN

loop_start:
	#check if the current command is zero
	cmp BYTE PTR [rbx], 0			# compare if the current first byte of command is zero
	# if yes  exit the loop and program
	je loop_end
	# if not then advance RBX so it points to the command argument
	# call a function that correspond to first byte of rbx 
	cmp BYTE PTR [rbx], '&'
	je EXECUTE_AND
	cmp BYTE PTR [rbx], '|'
	je EXECUTE_OR
	cmp BYTE PTR [rbx], 'S'
	je EXECUTE_SUB
	cmp BYTE PTR [rbx], 'U'
	je EXECUTE_UPPER
	cmp BYTE PTR [rbx], 'a'
	je EXECUTE_ARRAYSUB
	cmp BYTE PTR [rbx], 'l'
	je EXECUTE_LISTSUB
	cmp BYTE PTR [rbx], 'I'
	je EXECUTE_ATOQ
	cmp BYTE PTR [rbx], 'A'
	je EXECUTE_ARRAY
	cmp BYTE PTR [rbx], 'L'
	je EXECUTE_LIST
	jmp loop_start 

EXECUTE_AND:			# Execute and routine
	add rbx, 8
	call AND_FRAG
	jmp loop_start

EXECUTE_OR:			# Execute or routine
	add rbx, 8
	call OR_FRAG
	jmp loop_start

EXECUTE_SUB:			# Execute sub routine
	add rbx, 8
	call SUB_FRAG
	jmp loop_start

EXECUTE_UPPER:			# Execute upper routine
	add rbx, 8
	call UPPER_FRAG
	jmp loop_start

EXECUTE_ARRAYSUB:		# Execute arraysub routine
	add rbx, 8
	call ARRAYSUB_FRAG
	jmp loop_start

EXECUTE_LISTSUB:		# Execute listsub routine
	add rbx, 8
	call LISTSUB_FRAG
	jmp loop_start

EXECUTE_ATOQ:			# Execute atoq routine
	add rbx, 8
	call ATOQ_FRAG
	jmp loop_start

EXECUTE_ARRAY:			# Execute array routine
	call ARRAY_FRAG
	jmp loop_start

EXECUTE_LIST:			# Execute list routine
	call LIST_FRAG
	jmp loop_start
	
loop_end:			#exit the loop and program
	mov QWORD PTR [final_value], rax 	# move rax value to vairable
	mov rax, 1		# rax = system call number of write
	mov rdi, 1		# rdi = file descriptor number of standard output
	mov rsi, OFFSET final_value
	mov rdx, 8		# the number of bytes starting at the specified address to be written
	syscall

	mov rax, 1
	mov rdi, 1
	mov rsi, OFFSET SUB_POSITIVE # move SUB_POSITIVE address to rsi 
	mov rdx, 8
	syscall
	
	mov rax, 1
	mov rdi, 1
	mov rsi, OFFSET SUB_NEGATIVE # move SUB_NEGATIVE address to rsi
	mov rdx, 8
	syscall
	
	mov rax, 1
	mov rdi, 1
	mov rsi, OFFSET CALC_DATA_BEGIN
	# Calculate the number of bytes for the memory between CALC_DATA_BEGIN and CALC_DATA_END
	mov rdx, OFFSET CALC_DATA_END
	sub rdx, OFFSET CALC_DATA_BEGIN
	syscall
	
	mov rax, 60
	mov rdi, 0
	syscall
