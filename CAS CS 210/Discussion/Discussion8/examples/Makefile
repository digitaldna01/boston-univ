.PHONY: clean all

all: usesumit usecsumit csumit.s csum1 csum2 print

print: print.c
	gcc -o print -g print.c

usesumit: usesumit.o sumit.o
	ld -g usesumit.o sumit.o -o usesumit

usecsumit: usesumit.o csumit.o
	ld -g usesumit.o csumit.o -o usecsumit

sumit.o: sumit.s
	as -g sumit.s -o sumit.o

csumit.o: csumit.c
	gcc -g -c csumit.c 

csumit.s:
	gcc -fno-inline -fno-stack-protector -fno-pic  -static -Werror -fcf-protection=none -fno-asynchronous-unwind-tables -Os -S -masm=intel csumit.c -o csumit.s


csum1: csumit.o main1.o
	gcc --static -g -o csum1 csumit.o main1.o

csum2: csumit.o main2.o
	gcc --static -g -o csum2 csumit.o main2.o

main2.o: main2.c
	gcc --static -g -c main2.c

main1.o: main1.c
	gcc --static -g -c main1.c


usesumit.o: usesumit.s
	as -g usesumit.s -o usesumit.o

clean:
	-rm -rf $(wildcard *.o usesumit usecsumit csumit.s csum1 csum2 print)
