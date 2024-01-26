	.intel_syntax noprefix

	.section .text
	# tell linker that UPPER_FRAG symbols can be referenced in other files
	.global UPPER_FRAG
	# Code to change lowercase in string array to uppercase
	# UPPER_FRAG routine also counts the length of the string to rax
UPPER_FRAG:
	mov rdi, -1 			# Assign rdi = -1
	mov rdx, QWORD PTR [rbx] 	# Move string array address to rdx

loop_lowercase_start:
	inc rdi				# increase rdi by i everytime it loops
	cmp BYTE PTR [rdx + rdi], 0	# compare the current byte of the string
	je loop_lowercase_done		# if current byte is 0 then finish the loop
	cmp BYTE PTR [rdx + rdi], 'a'	# if the current charcter is smaller than 'a' then start the loop again
	jl loop_lowercase_start
	cmp BYTE PTR [rdx + rdi], 'z'	# if the current character is later than 'z' then start the loop again
	jg loop_lowercase_start
	sub BYTE PTR [rdx +rdi], 32 	# In order to make lowercase upper, subtract 32 in ascII code
	jmp loop_lowercase_start	# start the loop again for the next character

loop_lowercase_done:
	add rax, rdi			# Add rax the rdi value
	add rbx, 8			# Update rbx to next 8 bytes address
	ret				# Return back to where they get called from
