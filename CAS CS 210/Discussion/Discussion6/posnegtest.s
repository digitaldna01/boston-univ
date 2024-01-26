	.intel_syntax noprefix
	
	# switch to data section 
	.section .data 
data_start:            # use data_start label too mark beginning of array
	# each element is an 8 byte integer we use .quad
	# directive for each
	.quad 1           # first  element = 1
	.quad 2           # second element = 2
	.quad -4          # third  element = -4
	.quad 5           # fourth element = 5
	.quad 7           # fifth  element = 7
	.quad -13         # sixth  element = 13

	# switch to text section 
	.section .text

	# define global _start symbol so linker knows where our program
	# should begin executing
	.global _start
_start:
	xor rax, rax                         # rax = 0
	mov QWORD PTR [positive_count], rax  # set positive_count to 0
	mov QWORD PTR [negative_count], rax  # set negative_count to 0

	mov rax, OFFSET data_start           # set rax to address of
	                                     # first integer

	jmp loop_test                        # jump to our loop condition
loop_start:
	jmp POSNEG_FRAG
RETURN_HERE:
	inc rdi                              # increment loop index
loop_test:
	# compare index to length of array (5)
	cmp rdi, 5
        # if index <= length jump to top of loop
	jle loop_start                      

	# all done call OS exit system call
	mov rax, 60      # rax = 60 os exit system call number
	mov rdi, 0       # rdi = 0  exit status 0 success
	syscall          # call OS system call
