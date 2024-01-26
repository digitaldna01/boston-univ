	.intel_syntax noprefix

	.section .text
	# tell linker that AND_FRAG symbol can be referenced in other files
	.global AND_FRAG
	# code to run bitwise and operation of two inputs
	# take rax as x, rbx as addess of y for x bitwise and y operation
	# Update rbx to rbx bitwise and the first 16 bytes of rbx
	# Update rbx to rbx + 8 for next input array of rbx
	
AND_FRAG:	#label that marks where this code begins
	
	and rax, QWORD PTR [rbx]	# run x bitwise and y and save the result to x
	add rbx, 8 			# update rbx to next 8 bytes address
	int3				# give up and trap to the debugger 
	
	

