from constants import TOTAL_CORES
from mesi import Mesi
from dragon import Dragon
from core import Core
from snoop import Snoop



class Simulation:
    
    def __init__(self, protocol, input_file, cache_size, associativity, block_size):
        
        self.protocol = protocol.lower()
        if self.protocol == 'mesi':
            self.caches = [Mesi(cache_size, associativity, block_size, i) for i in range(TOTAL_CORES)]
        elif self.protocol == 'dragon':
            self.caches = [Dragon(cache_size, associativity, block_size, i) for i in range(TOTAL_CORES)]
        else:
            print('wrong command')

        self.cores = [Core(input_file, i, self.caches[i]) for i in range(TOTAL_CORES)]

    def execute(self):
        pass

    def results(self):
        pass



simulation = Simulation('mesi', 'blackscholes', 1024, 2, 16)
simulation.execute()
simulation.results()