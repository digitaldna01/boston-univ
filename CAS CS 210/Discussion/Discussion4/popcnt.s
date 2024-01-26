	.intel_syntax noprefix
	.text
	.global _start
_start:
	popcnt rax, rbx
	.byte 0xF3, 0x48, 0x0F, 0xB8, 0xD8
	int3
