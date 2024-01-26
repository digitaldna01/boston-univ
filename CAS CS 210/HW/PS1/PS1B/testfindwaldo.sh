#!/bin/bash
#set -x 
# A Simple script to help test a findwaldo script against a puzzle program

[[ -a puzzle1.sol ]] && puzzle1sol="$(cat puzzle1.sol)"
[[ -a puzzle2.sol ]] && puzzle2sol="$(cat puzzle2.sol)"
[[ -a puzzle3.sol ]] && puzzle3sol="$(cat puzzle3.sol)"
[[ -a puzzle4.sol ]] && puzzle4sol="$(cat puzzle4.sol)"

pgm=$1

# check we got at least one argument 
if [[ -z $pgm ]]; then
    echo "USAGE: $0 <puzzleprogram>"
    echo " run the findwaldo script against the specified puzzleprogram"
    echo " 1) check that both the findwaldo script exits and that the puzzleprogram exists"
    echo " 2) check that when run it produces the right output"
    exit -1
fi

# check 1: does the file exist
if [[ ! -a $pgm ]]; then
    echo "FAIL: $pgm does not exist."
    echo "0/1"
    exit -1
fi

# check 2: is the findwaldo script
if [[ ! -a findwaldo ]]; then
    echo "FAIL: findwaldo script does not exist ... did you commit and push your version of findwaldo?"
    echo "0/1"
    exit -1
fi

# check 4: when run does the program produce the right output
output=$(bash ./findwaldo $pgm)

referenceoutput=$(case $pgm in
    "puzzle1")
	echo "$puzzle1sol"
	;;
    "puzzle2")	
	echo "$puzzle2sol"
	;;
    "puzzle3")
	echo "$puzzle3sol"
	;;
    "puzzle4")
	echo "$puzzle4sol"
	;;
esac)

if [[ -z "$referenceoutput" ]]; then
    echo "I don't know anything about the output for $pgm"
    echo "... nice try ;-)"
    echo "?/10"
    exit -1
fi

if [[ "$output" == "$referenceoutput" ]]; then
    echo "Good job your program produces the correct output."
    echo PASS
    case $pgm in
	"puzzle1")
	    echo 20/20;;
	"puzzle2")
	    echo 20/20;;
	"puzzle3")
	    echo 30/30;;
	"puzzle4")
	    echo 10/10;;
	*)
	    echo 1/1;;
    esac
else
    if [[ -n "$referenceoutput" ]]; then
	echo "Sorry at this point your program does not produce the correct output."
	echo "Your program produced:"
	echo "$output"
	echo "It should have produced:"
	echo "$referenceoutput"
	echo "Remember this have to match exactly."
    fi
    echo FAIL
    echo 0/1
fi

