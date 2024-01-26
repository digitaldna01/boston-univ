if1: if1.o
	ld -g if1.o -o if1
if1.o: if1.s
	as -g if1.s -o if1.o
if2: if2.o
	ld -g if2.o -o if2
if2.o: if2.s
	as -g if2.s -o if2.o
loop1: loop1.o
	ld -g loop1.o -o loop1
loop1.o: loop1.s
	as -g loop1.s -o loop1.o
loop2: loop2.o
	ld -g loop2.o -o loop2
loop2.o: loop.s
	as -g loop2.s -o loop2.o
posnegtest: posnegtest.o posneg.o
	ld -g posnegtest.o posneg.o -o posnegtest
posneg.o: posneg.s
	as -g posneg.s -o posneg.o
posnegtest.o: posnegtest.s
	as -g posnegtest.s -o posnegtest.o

