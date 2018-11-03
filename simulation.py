from constants import MESI, DRAGON, WRONG_COMMAND, TOTAL_CORES
from mesi import Mesi
from dragon import Dragon
from core import Core
from snooping import Snooping

import sys

class Simulation:
    
    def __init__(self, protocol, input_file, cache_size, associativity, block_size):

        if protocol.lower() == MESI:
            self.protocol = Mesi
        elif protocol.lower() == DRAGON:
            self.protocol = Dragon
        else:
            sys.exit(WRONG_COMMAND)

        self.caches = [self.protocol(cache_size, associativity, block_size, i) for i in range(TOTAL_CORES)]
        self.cores = [Core(input_file, i, self.caches[i]) for i in range(TOTAL_CORES)]
        self.snooping = Snooping(self.caches)

    def execute(self):
        pass

    def results(self):
        pass



simulation = Simulation('mesi', 'blackscholes', 1024, 2, 16)
simulation.execute()
simulation.results()