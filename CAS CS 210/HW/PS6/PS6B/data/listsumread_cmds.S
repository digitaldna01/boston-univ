	.intel_syntax noprefix
	
	.data
	.global CALC_DATA_BEGIN
	.global CALC_DATA_END

CALC_DATA_BEGIN:	
	.byte 'r'
	.zero 7
	.quad 0

	.byte 'P'
	.zero 7
	.quad 0

	.byte 'r'
	.zero 7
	.quad 0
	
	.quad 0
	.quad 0
CALC_DATA_END:	
	
