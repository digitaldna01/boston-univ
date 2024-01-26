	.intel_syntax noprefix

	# switch to data section
	.section .data
	# set aside the memory for the two counters and make sure
	# the symbols are global so that they can be used in
	# posnegtest.s
	.global positive_count
	.global negative_count
positive_count:	 .quad 0      # set aside 8 bytes 
negative_count:	 .quad 0      # set aside 8 bytes

	.section .text

	# POSNEG_FRAG:
	# a little fragment of code that tests the 8 byte
	# signed integer number, x, pointed to by the address in rax.
	# NOTE: rax does not contain x but the address of x
	# INPUTS:
	#     rax -> &x address of where the value of x is in memory
	# OUTPUTS: if y is positive increment the positive_count
	#          else increment the negative_count
	#          finally rax should be updated to equal &x + 8
	#
	# This file must provide the global symbols
	# - positive_count : start of 8 bytes for postive count
	# - negative_count : start of 8 bytes for negative count
	# - POSNEG_FRAG    : starting instruction of the fragment

	# starting instruction label for the fragment
	.global POSNEG_FRAG
POSNEG_FRAG:
	# compare 8 byte value at the address in rax to 0
	cmp QWORD PTR [rax], 0
	# if negative (x<0) jump to negative case	
	jl is_neg                  
	# Positive Case:
	inc QWORD PTR [positive_count] # x>=0 increment positive_count
	# end of positive case goto conditon end
	jmp done_cond
	# Negative Case:
is_neg:	                               
	inc QWORD PTR [negative_count] # x<0 increment negative_count
	# Conditional logic ends here
done_cond:	                       
	add rax, 8       # update rax to point the next value
	# End of our Fragment
        int3             # use int3 to return to debugger 
	# will have use gdb to set pc to where we
	# want execution to go next : eg set $pc = <some label> 
