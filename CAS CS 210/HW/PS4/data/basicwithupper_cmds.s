	.intel_syntax noprefix
	
	.data
	.global CALC_DATA_BEGIN
	.global CALC_DATA_END

CALC_DATA_BEGIN:	
	.byte 'S'
	.zero 7
	.quad 123456789

	.byte '|'
	.zero 7
	.quad 0xdeadbeefdeadbeef

	.byte 'S'
	.zero 7
	.quad 1

	.byte 'S'
	.zero 7
	.quad 2
	
	.byte '&'
	.zero 7
	.quad 0xffffffff
	
	.byte 'U'
	.zero 7
	.quad STR0

	.byte 'S'
	.zero 7
	.quad -42
	
	.byte '|'
	.zero 7
	.quad -1

	.byte '&'
	.zero 7
	.quad 0x8000000000000000
	
	.byte 'U'
	.zero 7
	.quad STR1

	.byte '|'
	.zero 7
	.quad 0x1
	
	.quad 0
	.quad 0

STR0:	
	.ascii "Hello, this is a CrAzy string @a#b$C%d@e."
	.byte 0
STR1:
	.ascii "Tyger Tyger, burning bright,\n"
	.ascii "In the forests of the night;\n"
	.ascii "What immortal hand or eye,\n"
	.ascii "Could frame thy fearful symmetry?\n"
	.ascii "\n"
	.ascii "In what distant deeps or skies.\n"
	.ascii "Burnt the fire of thine eyes?\n"
	.ascii "On what wings dare he aspire?\n"
	.ascii "What the hand, dare seize the fire?\n"
	.ascii "\n"
	.ascii "And what shoulder, & what art,\n"
	.ascii "Could twist the sinews of thy heart?\n"
	.ascii "And when thy heart began to beat,\n"
	.ascii "What dread hand? & what dread feet?\n"
	.ascii "\n"
	.ascii "What the hammer? what the chain,\n"
	.ascii "In what furnace was thy brain?\n"
	.ascii "What the anvil? what dread grasp,\n"
	.ascii "Dare its deadly terrors clasp!\n"
	.ascii "\n"
	.ascii "When the stars threw down their spears\n"
	.ascii "And water'd heaven with their tears:\n"
	.ascii "Did he smile his work to see?\n"
	.ascii "Did he who made the Lamb make thee?\n"
	.ascii "\n"
	.ascii "Tyger Tyger burning bright,\n"
	.ascii "In the forests of the night:\n"
	.ascii "What immortal hand or eye,\n"
	.ascii "Dare frame thy fearful symmetry?\n";
	.byte 0
CALC_DATA_END:	
