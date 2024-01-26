#
# hmmm.py
#
# functions for assembling and running your Hmmm programs
#
# Computer Science 111
#
# You should *NOT* modify this file.
# Rather, you should do the following:
#
#     1. Run this file in IDLE, which will bring you to the Shell.
#
#     2. To assemble one of your HMMM files, call the assemble() function.
#        For example:
#
#        >>> assemble('ps5pr7.txt')
#
#        Doing so will create a .b file containing the assembled program.
#
#     3. To run one of your .b files, call the run() function.
#        For example:
#
#        >>> run('ps5pr7.b')
#

import hmc
from os.path import isfile

def assemble(file_name=None):
    if not file_name:
        file_name = input("Enter assembly file name: ")

    output_name = _strip_extension(file_name) + '.b'

    try:
        if not hmc.assemble(file_name, output_name):
            raise ValueError
    except IOError:
        print("error: could not find file", file_name)
        return
    except:
        print("error: assembly failed")
        return

    print("wrote binary program to", output_name)


def run(binary_name=None):
    if not binary_name:
        binary_name = input("Enter binary program file (.b) name: ")

    if not isfile(binary_name):
        print("error: could not find binary file", binary_name)
        print("did you run the assembler first?")
        return

    # should be the name of the file that generated this binary
    source_name = _strip_extension(binary_name) + '.txt'

    if isfile(source_name):
        # check that the source code is newer than this binary
        if _modify_time(source_name) > _modify_time(binary_name):
            print("warning: this binary program is older than its source")
            print("did you forget to run the assembler?")

    try:
        hmc.run(binary_name)
    except EOFError:
        print()
        print("*** stopped program ***")
    except SystemExit:
        print("*** program exited ***")


def _strip_extension(file_name):
    return ''.join(file_name.split('.')[:-1])


def _modify_time(file_name):
    from os import stat
    return stat(file_name).st_mtime

