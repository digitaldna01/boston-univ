#!/bin/bash
#set -x 
# Simple script help test calculator binaries and compare 
# their behavior to the reference implementation

binary=$1
reference=$2

# check we got at least one argument 
if [[ -z $binary ]]; then
    echo "USAGE: $0 <binary> [1]"
    echo " Make and run a calculator binary."
    echo " 1) Uses gdb to first gather an initial memory file <binary>.prebin"
    echo " 2) Then runs the binary to gather a <binary>.resbin file"
    echo " 3) Displays the changed bytes"
    echo " If the optional second argument is given the script will compare"
    echo " the changes against what the reference implementation produced."
    echo " The autograded portion will be based on the reference comparison"
    exit -1
fi

if [[ -a $binary ]]; then rm $binary; fi

if [[ -n *.o ]]; then rm *.o; fi

make $binary

if [[ ! -a $binary ]]; then
    echo "FAIL: $binary not made"
    echo "0/1"
    exit -1
fi

# Step A: use gdb to create a prebin file that contains zeros as the intial
#         values for : 1) RAX, 2) SUM_POSITIVE and 3) SUM_NEGATIVE
#         Also gather the intial values between CALC_DATA_BEGIN and
#         CALC_DATA_END
#         This prebin file will be used to compare the output the binary
#         writes to standard output. This way we see what changes it
#         produced

# delete output file if it exits
if [[ -a ${binary}.prebin ]]; then rm ${binary}.prebin; fi

# run gdb with commands feed from standard input
# using bash here docment support
# https://www.gnu.org/software/bash/manual/bash.html#Here-Documents
# both standard ouput and error are sent to /dev/null so things are quiet
echo "running gdb ... you will have to look in $0 to see what we are doing"
# Step A: set breakpoint and gather initial memory image (prebin)
# Step B: Run the binary to produce its version it final values for
#         values for : 1) RAX, 2) SUM_POSITIVE and 3) SUM_NEGATIVE
#         and the memory  values between CALC_DATA_BEGIN and
#         CALC_DATA_END
#         The program should write this too standard out.  We save
#         this output to a file resbin file

if [[ -a $binary.resbin ]]; then rm $binary.resbin; fi

if [[ -a $binary.stderr ]]; then rm $binary.stderr; fi

if [[ -a data/$binary.input ]]; then INPUT="< data/$binary.input"; else unset INPUT; fi

# gather values 
gdb $binary >/dev/null 2>&1 <<EOF
b _start
set args >$binary.resbin 2>$binary.stderr $INPUT
run 
dump binary value $binary.prebin {(long long)0, (long long)0, (long long)0}
append binary memory $binary.prebin &CALC_DATA_BEGIN &CALC_DATA_END
continue
quit
EOF

if [[ -a $binary.memreport ]]; then rm $binary.memreport; fi
   
# run valgrind to check for leaks
if [[ -a data/${binary}.input ]]; then 
    valgrind --leak-check=full \
             --show-leak-kinds=all \
             --track-origins=yes \
             --log-file=$binary.memreport \
             ./$binary 2>/dev/null >/dev/null < data/$binary.input
else
    valgrind --leak-check=full \
             --show-leak-kinds=all \
             --track-origins=yes \
             --log-file=$binary.memreport \
             ./$binary 2>/dev/null >/dev/null 
fi

if ! grep 'ERROR SUMMARY: 0 errors' $binary.memreport; then
    echo "FAILED MEMORY TEST:  You might have a leak problem see $binary.memreport"
    echo FAIL
    echo 0/1
    exit -1
else
    echo "passed memory check"
fi

changes=$(diff <(xxd -g1 $binary.prebin ) <(xxd -g1 $binary.resbin))

echo "The changes that $binary produced"
echo "$changes"

if [[ -n $reference ]]; then
    refbin=$binary
  
    if [[ ! -a data/reference_$refbin.prebin ]]; then
	refbin=${binary#c}
	if [[ ! -a data/reference_$refbin.prebin ]]; then
	    echo "ERROR: unable to find reference outputs in data dir"
	    exit -1
	fi
    fi
    
    if [[ -a data/reference_$refbin.stderr ]]; then
	if ! diff $binary.stderr data/reference_$refbin.stderr ; then
	    echo "Your $binary output to stander error does not match the reference"
	    echo "FAIL"
	    echo "0/1"
	    exit -1
	else
	    echo "passed standard error output test"
	fi
    fi

    refchanges=$(diff <(xxd -g1 data/reference_$refbin.prebin ) <(xxd -g1 data/reference_$refbin.resbin))
    if [[ $refchanges == $changes ]]; then
	echo "Good job your binary matches the behavior of the reference program"
	echo PASS
	echo 1/1
    else
	echo "Sorry at this point your binary does not match the reference program behavior"
	echo "Here are the changes the reference program makes to memory"
	echo "$refchanges"
	echo FAIL
	echo 0/1
    fi
fi

