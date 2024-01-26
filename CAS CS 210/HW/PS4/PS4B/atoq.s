	.intel_syntax noprefix

	.section .text
	# tell linker that ATOQ_FRAG symbols can be referenced on other files.
	.global ATOQ_FRAG
	# Code to loop through each values in the string character, and convert to integer
	# subtract the transfer value from rax
ATOQ_FRAG:
	xor rdi, rdi				# Assign rdi = 0
	xor rcx, rcx				# Assign rcx = 0
	xor rsi, rsi				# Assign rsi = 0
	mov rdx, QWORD PTR [rbx]		# Move String array address to rdx
	cmp BYTE PTR [rdx], '-' 		# check if the string value is a negative number
	jne loop_atoq_start		
	inc rdi
	
loop_atoq_start:
	movzx rcx, BYTE PTR [rdx + rdi]		# Move current string to rcx register
	cmp rcx, 48				# Check if the loop is done
	jl loop_atoq_done

	cmp rcx, 57				# Check if the loop is done
	jg loop_atoq_done

	sub rcx, 48
	imul rsi, 10				# multiply 10 for the next digits
	add rsi, rcx				# update total
	
	inc rdi					# increase index
	jmp loop_atoq_start			# Jump back to loop

loop_atoq_done:
	cmp BYTE PTR [rdx], '-'			# Check if the string integer is negative
	je negative_integer			
	add QWORD PTR [SUB_POSITIVE], rsi	# Update SUB_POSITIVE
	jmp done
	
negative_integer:
	imul rsi, -1
	sub QWORD PTR [SUB_NEGATIVE], rsi	# Update SUB_NEGATIVE
	jmp done

done:
	add rbx, 8				# Update rbx to next 8 bytes address
	sub rax, rsi				# Update rax value
	ret					# Return back to where the ATOQ get called from
