popcnt: popcnt.o # this command need popcnt.o file. if it doesnot have it then it will popcnt.o
	ld popcnt.o -o popcnt

popcnt.o: popcnt.s # this command need popcnt.s if it does not have then it can't make object file
	as popcnt.s -o popcnt.o

target: dependency_1 dependency_1
	recipe_command_1
	recipe_command_2
	recipe_command_3

add: add.o
	ld add.o -o add

add.o: add.s
	as add.s -o add.o
