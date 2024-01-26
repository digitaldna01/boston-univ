#!/bin/bash

# Simple script to test q3

#set -x

# delete the binary if it exits
if [[ -a empty ]]; then rm empty; fi

#make the binary
make empty

if [[ ! -a empty ]]; then
    echo "FAIL: empty not made"
    echo "0/1"
    exit -1
fi

# delete output file if it exist 
if [[ -a q3.resbin ]]; then rm q3.resbin; fi

# run gdb with commands feed from standard input
# using bash here docment support
# https://www.gnu.org/software/bash/manual/bash.html#Here-Documents
# both standard ouput and error are sent to /dev/null so things are quiet
gdb empty >/dev/null 2>&1  <<EOF
set disassembly-flavor intel
source q3.gdb
b _start
run
delete 1
q3
set \$rax = -1
set \$rip = _start
si
si
dump binary value q3.resbin { \$rax, \$rbx, *((long long *)\$rip) }
EOF

sol='ffffffffffffffff00000000000000000000000000000000'

if [[ $(xxd -p q3.resbin) == $sol ]]; then
    echo PASS
    echo 1/1
else
    echo FAIL
    echo 0/1
fi
