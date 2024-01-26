	.intel_syntax noprefix
	
	.data
	.global CALC_DATA_BEGIN
	.global CALC_DATA_END

CALC_DATA_BEGIN:	
	.byte 'L'
	.byte 'S'
	.zero 6
	.quad HEAD_NODE

	.quad 0
	.quad 0

	.string "THIS IS PADDING"

NODE_1:
	.quad 1
	.quad NODE_8

NODE_2:
	.quad 2
	.quad NODE_3

NODE_3:
	.quad 3
	.quad NODE_1

NODE_4:
	.quad 4
	.quad NODE_2

NODE_5:
	.quad 5
	.quad 0

NODE_6:
	.quad -1
	.quad NODE_7

NODE_7:
	.quad -2
	.quad NODE_9

NODE_8:
	.quad -3
	.quad NODE_6

NODE_9:
	.quad -4
	.quad NODE_5

HEAD_NODE:
	.quad -5
	.quad NODE_4

CALC_DATA_END:	
	
