andtest: andtest.o and.o
	ld -g andtest.o and.o -o andtest
andtest.o: andtest.s
	as -g andtest.s -o andtest.o
and.o: and.s
	as -g and.s -o and.o
ortest: ortest.o or.o
	ld -g ortest.o or.o -o ortest
ortest.o: ortest.s
	as -g ortest.s -o ortest.o
or.o: or.s
	as -g or.s -o or.o
subtest: subtest.o sub.o
	ld -g subtest.o sub.o -o subtest
subtest.o: subtest.s
	as -g subtest.s -o subtest.o
sub.o: sub.s
	as -g sub.s -o sub.o
