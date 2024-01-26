	.intel_syntax noprefix

	.section .text
	# tell linker that OR_FRAG symbol can be referenced in other files
	.global OR_FRAG
	# code to tun bitwise or of two inputs
	# take rax as x, rbx as address of y for x bitwise or y operation
	# Update rbx to rbx bitwise or the first 16 bytes of rbx
	# Update rbx to rbx + 8 for next input array of rbx

OR_FRAG:	# label that marks where this code begins
	or rax, QWORD PTR [rbx]		# run x bitwise or y and save the result to x
	add rbx, 8			# update rbx to next 8 bytes address
	int3				# give up and trap to the debugger
