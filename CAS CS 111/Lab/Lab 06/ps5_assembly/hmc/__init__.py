from imp import reload

import hmc.hmmmAssembler
import hmc.hmmmSimulator

def assemble(file_name, output_name):
    reload(hmc.hmmmAssembler)
    return hmc.hmmmAssembler.main(file_name, output_name)

def run(file_name):
    reload(hmc.hmmmSimulator)
    hmc.hmmmSimulator.main(['-f', file_name])
