dummy: data/basic_cmds.o dummy.o
	ld -g dummy.o data/basic_cmds.o -o dummy
data/basic_cmd.o: data/basic_cmd.s
	as -g data/basic_cmd.s -o data/basic_cmds.o
dummy.o: dummy.s
	as -g dummy.s -o dummy.o

calc_basic: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/basic_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/basic_cmds.o -o calc_basic
calc_simpleone: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/simpleone_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/simpleone_cmds.o -o calc_simpleone
calc_upperonly: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/upperonly_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o  atoq.o array.o list.o data/upperonly_cmds.o -o calc_upperonly
calc_easy: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/easy_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/easy_cmds.o -o calc_easy
calc_basicwithupper: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/basicwithupper_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/basicwithupper_cmds.o -o calc_basicwithupper
calc_simplerandom: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/simplerandom_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/simplerandom_cmds.o -o calc_simplerandom
calc_arraysub: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/arraysub_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/arraysub_cmds.o -o calc_arraysub
calc_listsub: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/listsub_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/listsub_cmds.o -o calc_listsub
calc_atoq: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/atoq_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/atoq_cmds.o -o calc_atoq
calc_array: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/array_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/array_cmds.o -o calc_array
calc_list: calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/list_cmds.o
	ld -g calc.o and.o or.o sub.o upper.o arraysub.o listsub.o atoq.o array.o list.o data/list_cmds.o -o calc_list

calc.o: calc.s
	as -g calc.s -o calc.o
and.o: and.s
	as -g and.s -o and.o
or.o: or.s
	as -g or.s -o or.o
sub.o: sub.s
	as -g sub.s -o sub.o
upper.o: upper.s
	as -g upper.s -o upper.o
arraysub.o: arraysub.s
	as -g arraysub.s -o arraysub.o
listsub.o: listsub.s
	as -g listsub.s -o listsub.o
atoq.o: atoq.s
	as -g atoq.s -o atoq.o
array.o: array.s
	as -g array.s -o array.o
list.o: list.s
	as -g list.s -o list.o

data/basic_cmds.o: data/basic_cmds.s
	as -g data/basic_cmds.s -o data/basic_cmds.o
data/simpleone_cmds.o: data/simpleone_cmds.s
	as -g data/simpleone_cmds.s -o data/simpleone_cmds.o
data/upperonly_cmds.o: data/upperonly_cmds.s
	as -g data/upperonly_cmds.s -o data/upperonly_cmds.o
data/easy_cmds.o: data/easy_cmds.s
	as -g data/easy_cmds.s -o data/easy_cmds.o
data/simplerandom_cmds.o: data/simplerandom_cmds.s
	as -g data/simplerandom_cmds.s -o data/simplerandom_cmds.o
data/arraysub_cmds.o: data/arraysub_cmds.s
	as -g data/arraysub_cmds.s -o data/arraysub_cmds.o
data/listsub_cmds.o: data/listsub_cmds.s
	as -g data/listsub_cmds.s -o data/listsub_cmds.o
data/atoq_cmds.o: data/atoq_cmds.s
	as -g data/atoq_cmds.s -o data/atoq_cmds.o
data/array_cmds.o: data/array_cmds.s
	as -g data/array_cmds.s -o data/array_cmds.o
data/list_cmds.o: data/list_cmds.s
	as -g data/list_cmds.s -o data/list_cmds.o
