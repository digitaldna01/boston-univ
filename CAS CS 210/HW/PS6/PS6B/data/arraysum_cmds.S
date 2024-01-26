	.intel_syntax noprefix
	
	.data
	.global CALC_DATA_BEGIN
	.global CALC_DATA_END

CALC_DATA_BEGIN:	
	.byte 'a'
	.zero  7
	.quad  (argarray_end - argarray)/8
	.quad  argarray

	.quad 0
	.quad 0

	.string "THIS IS PADDING AGAIN AND AGAIN"
	
argarray:
	.quad 2
	.quad 3
	.quad 8
	.quad -8
	.quad 5
	.quad -13
	.quad 4
	.quad -7
	.quad 6
	.quad 9
	.quad 1
	.quad 18
argarray_end:
	
CALC_DATA_END:	
