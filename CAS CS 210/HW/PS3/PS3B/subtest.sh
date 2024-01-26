#!/bin/bash
#set -x 
# Simple script to test the sub assembly fragment

# assemble subtest.S into subtest.o
if [[ -a subtest.o ]]; then rm subtest.o; fi
make subtest.o
# assemble sub.S into sub.o
if [[ -a sub.o ]]; then rm sub.o; fi
make sub.o
# link subtest.o and sub.o into subtest
if [[ -a subtest ]]; then rm subtest; fi
make subtest

if [[ ! -a subtest ]]; then
    echo "FAIL: subtest not made"
    echo "0/1"
    exit -1
fi

# delete output file if it exits
if [[ -a sub.resbin ]]; then rm sub.resbin; fi

# run gdb with commands feed from standard input
# using bash here docment support
# https://www.gnu.org/software/bash/manual/bash.html#Here-Documents
# both standard ouput and error are sent to /dev/null so things are quiet
echo "running gdb ... you will have to look in $0 to see what we are doing"

gdb subtest >/dev/null 2>&1 <<EOF
b _start
run
delete 1
set \$rip=test1
c
dump binary value sub.resbin { \$rax, *((long long *)&SUB_POSITIVE), *((long long *)&SUB_NEGATIVE) }
set \$rip=test2
c
append binary value sub.resbin { \$rax, *((long long *)&SUB_POSITIVE), *((long long *)&SUB_NEGATIVE) }
set \$rip=test3
c
append binary value sub.resbin { \$rax, *((long long *)&SUB_POSITIVE), *((long long *)&SUB_NEGATIVE) }
set \$rip=test4
c
append binary value sub.resbin { \$rax, *((long long *)&SUB_POSITIVE), *((long long *)&SUB_NEGATIVE) }
quit
EOF

if [[ $(xxd -ps -g8 sub.resbin) == 'ffffffffffffffff01000000000000000000000000000000cf1100000000
00000100000000000000d011000000000000632bdefcffffffff6de62103
00000000d011000000000000652bdefcffffffff6de6210300000000d211
000000000000' ]]; then
    echo PASS
    echo 1/1
else
    echo FAIL
    echo 0/1
fi
