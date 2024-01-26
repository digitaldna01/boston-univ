#!/bin/bash

# simple script to test q4

# set -x

# delete the binary if it exits
if [[ -a empty ]]; then rm empty; fi

# make the binary
make empty

if [[ ! -a empty ]]; then
	echo "FAIL: empty not made"
	echo "0/1"
	exit -1
fi

# delete output file if it exist
if [[ -a q4.resbin ]]; then rm q4.resbin; fi

# run gdb with commands feed from standard input
# using bash here docment support
# https://www.gnu.org/software/bash/manual/bash.html#Here-Documents
# both standard ouput and error are sent to /dev/null so things are quiet
gdb empty >/dev/null 2>&1  <<EOF
set disassembly-flavor intel
source q4.gdb
b _start
run
delete 1
q4
set \$rax = 0x0f0f
set \$rip = _start
si
p /u \$rbx
dump binary value q4.resbin { \$rbx }
q4
set \$rax = -11
set \$rip = _start
si
append binary value q4.resbin { \$rbx }
q4
set \$rax = 0xfade1aaa000f
set \$rip = _start
si
append binary value q4.resbin { \$rbx }
EOF

sol='08000000000000003e000000000000001700000000000000'

if [[ $(xxd -p q4.resbin) == $sol ]]; then
	echo PASS
	echo 1/1
else
	echo FAIL
	echo 0/1
fi
