	.intel_syntax noprefix
	.section .text
	.global _start
_start:
test1:
	mov rbx, OFFSET data_start
	xor rax, rax
	jmp OR_FRAG
test2:
	jmp OR_FRAG
test3:
	jmp OR_FRAG

	.section .data
data_start:
	.quad 0x8000000000000001 # outside bits
	.quad 0x000000FFFF000000 # middle 16 bits
	.quad 0x6F3A823BE019DD45
data_end:
	.quad 0x0
