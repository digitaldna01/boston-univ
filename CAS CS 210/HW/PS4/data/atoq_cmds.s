	.intel_syntax noprefix
	
	.data
	.global CALC_DATA_BEGIN
	.global CALC_DATA_END

CALC_DATA_BEGIN:	
	.byte 'I'
	.zero 7
	.quad NUM1

	.byte 'I'
	.zero  7
	.quad NUM2

	.byte 'I'
	.zero 7
	.quad NUM3

	.byte 'I'
	.zero 7
	.quad NUM4

	.quad 0
	.quad 0

NUM3:	.string "42 00"
NUM1:	.string "5"
NUM2:	.string "-23"
NUM4:	.string "-44"
	
CALC_DATA_END:	
