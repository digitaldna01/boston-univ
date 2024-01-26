	.intel_syntax noprefix
	.section .text
	.global _start
_start:
test1:
	xor rax, rax
	mov QWORD PTR [SUB_POSITIVE], rax
	mov QWORD PTR [SUB_NEGATIVE], rax

	mov rbx, OFFSET data_start

	jmp SUB_FRAG
test2:
	jmp SUB_FRAG
test3:
	jmp SUB_FRAG
test4:
	jmp SUB_FRAG

	.section .data
data_start:
	.quad 1
	.quad -4560
	.quad 52553324
	.quad -2
data_end:
	.quad 0x0
