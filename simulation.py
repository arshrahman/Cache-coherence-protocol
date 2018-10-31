from mesi import Mesi
from dragon import Dragon
from core import Core
from snoop import Snoop



class Simulation:
    
    def __init__(self, protocol, input_file, cache_size, associativity, block_size):
        
        self.protocol = protocol.lower()
        if self.protocol == 'mesi':
            self.caches = [Mesi(cache_size, associativity, block_size, i) for i in range(4)]
        elif self.protocol == 'dragon':
            self.caches = [Dragon(cache_size, associativity, block_size, i) for i in range(4)]
        else:
            print('wrong command')

    def execute(self):
        pass

    def results(self):
        pass



sim = Simulation('mesi', 'blackscholes', 4096, 2, 32)
sim.execute()
sim.results()