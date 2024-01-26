	.intel_syntax noprefix
	
	.data
	.global CALC_DATA_BEGIN
	.global CALC_DATA_END

CALC_DATA_BEGIN:	
	.byte 'p'
	.zero 7
	.quad -1

	.byte 'p'
	.zero 7
	.quad 1

	.byte 'p'
	.zero 7
	.quad 0
	
	.byte 'p'
	.zero 7
	.quad 0xaaaaaaaaaaaaaaaa
	
	.quad 0
	.quad 0
CALC_DATA_END:	
	
