#!/bin/bash

# Simple script to test q1

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
if [[ -a and.resbin ]]; then rm and.resbin; fi

# run gdb with commands feed from standard input
# using bash here docment support
# https://www.gnu.org/software/bash/manual/bash.html#Here-Documents
# both standard ouput and error are sent to /dev/null so things are quiet
gdb empty >/dev/null 2>&1  <<EOF
source q1.gdb
b _start
run
q1
p/t { \$rax,\$rbx,\$rcx,\$rdx,\$r8 }
dump binary value q1.resbin { \$rax,\$rbx,\$rcx,\$rdx,\$r8 }
EOF

sol='59000000000000002d00000000000000d2000000000000004e0000000000
0000e900000000000000'

if [[ $(xxd -p q1.resbin) == $sol ]]; then
    echo PASS
    echo 1/1
else
    echo FAIL
    echo 0/1
fi
