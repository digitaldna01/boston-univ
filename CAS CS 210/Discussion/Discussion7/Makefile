.PHONY: clean all

all: string flowers stdout1 stdout2 stdoutflowers

string: string.o
	ld -g string.o -o string

string.o: string.s
	as -g string.s -o string.o

flowers: flowers.o
	ld -g flowers.o -o flowers

flowers.o: flowers.s
	as -g flowers.s -o flowers.o

stdout1: stdout1.o
	ld -g stdout1.o -o stdout1

stdout1.o: stdout1.s
	as -g stdout1.s -o stdout1.o

stdout2: stdout2.o
	ld -g stdout2.o -o stdout2

stdout2.o: stdout2.s
	as -g stdout2.s -o stdout2.o

stdoutflowers: stdoutflowers.o
	ld -g stdoutflowers.o -o stdoutflowers

stdoutflowers.o: stdoutflowers.s
	as -g stdoutflowers.s -o stdoutflowers.o
clean:
	-rm -rf $(wildcard *.o string flowers stdout1 stdout2 stdoutflowers)
