# PS1B: Finding Waldo

## Overview

In this assignment we will be playing our own geeky version of
[Where's Waldo?](https://en.wikipedia.org/w/index.php?oldid=1103610587).


This will exercise our basic knowledge of UNIX and the shell.  This will also
help to familiarize us with working in the terminal environment.

You are given four binary executables called `puzzle1`, `puzzle2`, 
`puzzle3` and `puzzle4`.  Each binary is a program that produces "pages" of output.  Each
program can be run by executing them via a shell command-line composed
of their name followed by a single integer argument, that specifies a "page",
within the inclusive range of 0-99.

Eg.
```
$ ./puzzle1 27
```

Runs the `puzzle1` binary passing in 27 as the "page" number.

For a given "page" number each puzzle binary will produce three kinds of output:

1. ascii lines of text to its standard output stream
2. ascii lines of text to its standard error stream
3. ascii lines of text to a set of files it creates in a directory called "PuzzleDir".

For each of these output types the binary might or might not create "waldo instances".
Later in the writeup we will discuss what exactly "waldo instances" are.

After exploring the puzzles by hand your job will be to develop a
shell script, called `findwaldo`,  that automates solving a puzzle.
To solve a puzzle you must do the following:
1. Identify all the page numbers for which a puzzle binary produces "waldo instances"
2. For page numbers that a binary produces "waldo instances" you must count each type

Eg.  The solution to  `puzzle1` is: `puzzle1 37 9 0 0 0`

Which means:

1. It only produces "waldo instances" for page number 37
2. On page 37 it produces 9 "standard output waldos" and no others

More details regarding the puzzles and their solutions are provided below.

In addition to reviewing your code and git histories, we will evaluate
your `findwaldo` script by running it on the three given puzzle
binaries for which you have the solutions, and the fourth puzzle that
you don't have the solution for.

## What we will be exploring

Part of what makes UNIX and the shell so powerful is our ability
to easily automate tasks.

In this assignment we will explore how to:

1. Use a shell command-line to run a process from a given executable file.
2. Redirect and examine the standard output and error of a process looking for a particular string
3. Search a body of ASCII files within a tree of directories for a string
4. Find all occurrences of a file of a particular name

As we do the above we will reinforce various UNIX and shell ideas
along with learning how to work effectively in the UNIX terminal
environment.

## The Puzzles Binaries

**DO NOT START BY TRYING TO WRITE THE SCRIPT**

Explore the puzzle binaries by running them by hand.  You will find
that each time you run one of the binaries it will produce lots of
lines of ASCII text and create a number of files and directories.

Each of the given binaries will, for a particular value of the integer
"page" number passed to it,  generate  "waldo instances".

Our job is to be able to figure out, for a given binary, 
which integer "page" values the binary produces "waldo instances" and
how many of each type is generated.

### "waldo instances"

An instance of "waldo" is a line of text that contains the string
"waldo".  However, any mix of capitalization counts as an instance of
"waldo".  Eg. "waldo", "WalDO", "Waldo", etc. all count as an
instance of waldo.

#### standard output waldo instances

Your job is to run a puzzle binary and search what it prints to its
standard output stream looking for "waldo instances" and count them.
We think of these as "standard output waldo instances"

#### standard error waldo instances

Similarly you need to do the same for the what the binary prints to
its standard error stream.  These are "standard error waldo instances".

Once you have figured out how to find and count the "standard output
waldo instances" and the "standard error waldo instances", you can
move on to the last two types of "waldo instances".


#### file line waldo instances

Each puzzle binary will also create a tree of directories
under a directory called "PuzzleDir".  Within this tree it will create
files that contain ASCII lines of text.  Some of these files might
contain "waldo instances".  We call this type of "waldo instance",
"file line waldo instances".  You job is to find count all of them.


#### file name waldo instances

The final kind of "waldo instance" you need to find are files within
the `PuzzleDir` whose name matches the "waldo" string.  Again a
"waldo" file might be named with any mix of capitalization.  Eg. A
file named "waldo" or "WaLdO" or "WALdo", etc would all count as waldo
instances.  We call this type of "waldo instance" a "file name waldo
instances".


### Puzzle solutions

A solution to a puzzle binary is a set of lines 
that identify a page number for which the binary produced "waldo
instances" followed by the count of each of the four types.


For `puzzle1`, `puzzle2` and `puzzle3` we have provided you the
'solutions' in the files called `puzzle1.sol`, `puzzle2.sol` and
`puzzle3.sol`.  If you look at the contents of these files it will
tell you the integer page number parameter that, when passed to the puzzle binary,
will produce "waldo" instances and how many of each type

Eg.

```
$ cat puzzle1.sol
puzzle1 37 9 0 0 0
$ cat puzzle2.sol
puzzle2 63 1 27 0 0
$ cat puzzle3.sol
puzzle3 12 3 0 0 0
puzzle3 43 0 5 0 0
puzzle3 88 0 0 7 1
$
```

The solution file, `puzzle3.sol`, tells us that there are three "page" numbers, '12',
'43' and '88' that the `puzzle3` binary produces "waldo instances" on.

The four numbers following the page number are the counts of each type
in the following order: "standard output waldo instances", "standard
error waldo instances", "file line waldo instances" and finally "file
name waldo instances".

## Exploring a puzzle

A puzzle binary is a UNIX binary executable file.  We encourage you to
use UNIX commands to "examine" them a little.  Eg. Use "ls -l" to look
at their meta data.  Remember they are binary files so the data in
them is NOT ASCII lines.  So while you can try using `cat` on the binaries
their contents will not make sense in the terminal.  However, you can use a
program like "hexdump" if you like to try and look at their bytes of contents as
hexadecimal numbers.


### Running a puzzle binary

The main thing to do with the puzzle binaries is to run them.  To do
this you need to issue a command line that causes the shell to find
and execute a puzzle binary as an external command. See the appropriate section of the
textbook to learn what this means.

The following is an example of running the `puzzle1` binary passing in 0 as the page number.

```
$ ./puzzle1
USAGE: ./puzzle1 <n>
     Where n is an integer value with 0<=n<=99.
$ ./puzzle1 0
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
I am not here...
$ 
```

As discussed a puzzle binary, when run, will also create a tree of
directories and files in a directory called `PuzzleDir`.  Running `ls
PuzzleDir` after running `./puzzle1 0` confirms this.

```
$ ls PuzzleDir/
2088_mystery_0  2088_mystery_3  2108_mystery_0  2108_mystery_3  mystery_0  mystery_3  mystery_6
2088_mystery_1  2088_mystery_4  2108_mystery_1  2108_mystery_4  mystery_1  mystery_4  mystery_7
2088_mystery_2  2088_mystery_5  2108_mystery_2  2108_mystery_5  mystery_2  mystery_5  mystery_8
$
```

Remember every time you run a puzzle binary it will create more
contents in the PuzzleDir.  So to avoid getting confused you will want
to figure out how to remove `PuzzleDir` and all the contents under
it before running a puzzle binary again.

Now you need to start poking around. Here are several to try:

1. See if you can figure out how to use redirection to save the output for standard output to a file.
2. See if you can figure out how to look at the contents of the output you save.
3. Try running the `puzzle1` binary with the page number that it creates instances of standard output waldos (see `puzzle1.sol`)
4. Can you find and count standard out waldos?
5. Using `puzzle2` can you do the same for standard error waldos?
6. Explore the contents of the `PuzzleDir` by hand (Use `cd`, `ls` and `cat`).
7. Learn to use some commands to print all the directories and files of the `PuzzleDir`
8. Figure out how to search and count the "file line waldo instances" of `puzzle3`
 
## findwalo script

At this point you should have a good idea of how to, by hand, use
interactive shell command lines in a terminal window, to detect and
count the waldo instances of a puzzle binary.  Now your task is to
learn how to use a terminal text based editor and `git` to develop a
shell script called `findwaldo`.



## findwaldo

Your findwaldo should take one command line argument and print
the solution to the specified binary to its standard output.

Eg.
```
$ ./findwaldo puzzle1
puzzle1 37 9 0 0 0
$
```

Notice its output exactly matches the contents of `puzzle1.sol` file.

The provides `testfindwaldo.sh` script is a simple shell script that runs your
`findwaldo` script on the specified puzzle and compares your output to that of the solutions.
Eg.

```
$ ./testfindwaldo.sh puzzle1
Good job your program produces the correct output.
PASS
20/20
$
```

Each puzzle has a different point value associated with solving it.
See the Evaluation section of this writeup for more details.

On gradescope we will use the `testfindwaldo.sh` for the autograded
portion of your problem set grade.  We encourage you read the
`testfindwaldo.sh` shell script.

### ASCII text editor

Learn to use an ascii terminal based text editor in the UNIX environment to
create and develop your `findwaldo` script.

There are a few editors we have installed.  The two most common UNIX terminal based editors are
`emacs` and `vim`.  Take a look on Piazza for some howto's regarding getting started with
editing ASCII files in UNIX.

1. learn to start an editor in a new terminal window
2. learn to open a file in the editor
3. learn to insert and edit ASCII lines in the editor
4. learn to save the contents
5. learn to exit the editor.

In general you will want to have a second terminal window open to constantly be testing your script and to use git.

### git

As you develop your `findwaldo` script you MUST use git to record and document your progress.
As part of the grading we will be looking at your git histories to examine how and when you conducted your work.

See piazza for some help with the basic git commands you will need.

Here is a very quick summary:

#### `git add <file>`

Eg. `git add findwaldo` -- this adds your current version of your script to the "stage" in preparation for the next steps of committing and pushing.

#### `git commit -m "commit message"`

Eg. `git commit -m "Starting work on my findwaldo script"` -- this adds a timestamped record of this change to the history in your local copy of your assignment git repository.


#### `git push`

This updates the main copy of your assignment repository on github classroom with the local version you are working on in the UNIX environments.

#### `git clone <repository url>`

Note every time you work on your assignment you will need to login to
the UNIX environment and get a new local copy of your assignment
repository using the `git clone` command.  See Piazza for help.


#### `git status`

`git status` -- tells you the current state of your local copy
relative to the main version on github.  Eg it can tell you if you
have changes that are not recorded and pushed.  Before you stop work
you should always run `git status` to make sure you have saved,
committed and pushed all your work.  You might also want to check on
the github website to ensure all your work has been saved.


#### `git log --decorate --oneline --graph --all`

The `git log --decorate --oneline --graph --all` command shows you a
summary of all the commits, records of work, in your repository.


The following is the version of the git log command that we will use
to examine your git histories for grading.

```
git log --graph --all --pretty=format:'%C(auto)%h%d (%ci) %ce %s'
```


## Evaluation / Grading

Total score : 100

1. 80 points for autograded evaluation of your `findwaldo` script
    1. 20 points for solving `puzzle1`
    2. 20 points for solving `puzzle2`
    3. 30 points for solving `puzzle3`
    4. 10 points for solving `puzzle4`  (note you do not have the solution file for puzzle 4)
2. 20 points for manual grading:
    1. 10 points for documenting and explain each line of your script using comment lines
    2. 10 points for having a "correct" git history
       1. several commits that document your work.
       2. At least four commits that indicated when you began adding support for one of the waldo instance types. 
           1. These commits should have the following commit messages:
               1. "adding support for standard output waldos"
               2. "adding support for standard error waldos"
               3. "adding support for file line waldos"
               4. "adding support for file name waldos"

**GIT Histories:** If we do not see a sufficient git history that
   documents your effort we will assign you a grade of zero for the
   autograding score.  A sure fire way of triggering this rule is
   submitting a solution with only one or two commits.  Particularly
   suspicious histories are ones in which a small number of commits
   occur in a very short span of time, often just before the deadline,
   that shows your repository going from no solution to a working
   solution.

If you start early and work at a regular interval and frequently document your
progress with commits you will be fine.  Commit every time you try something.
Even if it does not work.  Eg.  `git commit  -m "still broken getting file does not exist errors :-("`

Here is a shortened example of a git history for a solution:

```
$ git log --graph --all --pretty=format:'%C(auto)%h%d (%ci) %ce %s'
* 628403e (HEAD -> main, origin/main, origin/HEAD) (2022-08-29 19:32:31 +0000) jappavoo@bu.edu fix fixed typeos in comments
* 45ffb9c (2022-08-29 19:29:16 +0000) jappavoo@bu.edu added exit status optimization
* fc4540d (2022-08-29 13:27:59 -0400) jappavoo@bu.edu fixed bug in file name waldo instances counting
* f8678ff (2022-08-29 11:37:07 -0400) jappavoo@bu.edu adding support for file name waldos
* bd1b791 (2022-08-27 15:49:45 +0000) jappavoo@bu.edu fixed bug with variable assignment
* a09c64f (2022-08-27 11:28:52 -0400) jappavoo@bu.edu added printing of file line waldo count  
* fb5e753 (2022-08-25 21:12:26 +0000) jappavoo@bu.edu added missing option for case insensitive
* f02e8d8 (2022-08-25 11:19:33 +0000) jappavoo@bu.edu fixed options to search recursively
* 870d546 (2022-08-25 02:46:18 +0000) jappavoo@bu.edu added search of PuzzleDir 
.
.
.
* ca51fcd (2022-08-25 02:14:43 +0000) jappavoo@bu.edu adding support for file line waldos
* 55268f8 (2022-08-23 22:56:00 +0000) jappavoo@bu.edu fixed incorrect loop bounds
* bab09dc (2022-08-23 16:22:04 +0000) jappavoo@bu.edu fixed clearing of counts each iteration
* 94aea23 (2022-08-19 22:22:55 +0000) jappavoo@bu.edu added command to print results
* 95ad169 (2022-04-26 23:19:00 +0000) jappavoo@bu.edu added variables for counts
* b883ad8 (2022-04-25 21:52:56 +0000) jappavoo@bu.edu fixed cleanup of standard error and out files
* e5c28b8 (2022-04-25 21:51:43 +0000) jappavoo@bu.edu added search of standard error file
* d48116a (2022-04-25 19:54:39 +0000) jappavoo@bu.edu got standard error redirection working 
.
.
.
* c6625cc (2022-03-22 14:49:00 +0000) jappavoo@bu.edu adding support for standard error waldos
* 8fa61f7 (2022-03-22 04:28:54 +0000) jappavoo@bu.edu fixed case sensitivity bug
* 7b4f471 (2022-03-19 14:06:26 +0000) jappavoo@bu.edu added cleanup of PuzzleDir 
* cd03a24 (2022-03-19 12:59:19 +0000) jappavoo@bu.edu fixed bug where file was appended to each iteration
* b05a42d (2022-03-19 08:44:39 +0000) jappavoo@bu.edu added command to search standard out for waldos
* cfe35c2 (2022-03-16 18:15:26 +0000) jappavoo@bu.edu added redirection of standard out to a file
* 49126d2 (2022-03-14 14:40:52 +0000) jappavoo@bu.edu adding support for standard output waldos
* b2d087a (2022-03-11 14:27:21 -0500) jappavoo@bu.edu added support for passing puzzle name as input
* 9ca6d75 (2022-03-04 22:19:53 +0000) jappavoo@bu.edu implemented loop structure 

```

## Files

- `README.md` : this file
- `puzzle1` : the first puzzle binary - produces standard output waldos
- `puzzle1.sol` : solution file for `puzzle1`
- `puzzle2` : the second puzzle binary - produces standard error waldos
- `puzzle2.sol` : solution file for `puzzle2`
- `puzzle3` : the third puzzle binary - produces all four kinds of waldos
- `puzzle3.sol` : solution file for `puzzle3`
- `puzzle4` : the fourth puzzle binary - the mystery puzzle - no solution provided
- `.gitignore` : we provide you a "gitignore" file to ensure that only the `findwaldo` file gets committed

## Hints

The online textbook covers all of the material and skills you will need to complete this problem set.

- The following commands are really useful:
   - `grep`
   - `wc`
   - `find`
- pipelines are your friend
- the shell `for` internal command has support for arithmetic expansion
  - `for ((i=0; i<10; i++)); do echo $i; done`
- `rm` has flags that let you do a recursive deleting
- Command substitution is really useful for setting a variable to the standard output of a command
  - Eg. `numusers=$(cat /etc/passwd | wc -l); echo $numusers`

When you get to writing your `findwaldo` script you might find these textbook sections particularly helpful:
- "4.7.4.1.4. Command Substitution"
- "4.7.5 Parse Redirections"
- "4.8.2 Pipelines"
- "4.8.4.1 Loops"
- "4.8.4.2 Conditionals"
