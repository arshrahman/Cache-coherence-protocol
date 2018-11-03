from constants import MESI, DRAGON, WRONG_COMMAND, TOTAL_CORES, LOAD, STORE, OTHER, COUNT
from mesi import Mesi
from dragon import Dragon
from core import Core
from snooping import Snooping

import sys
import time

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
        counter = 0
        done = [False for i in range(TOTAL_CORES)]
        start_time = time.time()

        while not all(done):
            snooping_busy = self.snooping.is_busy()
            for c in self.cores:
                if done[c.core_num]:
                    c.instruction_type[COUNT] = counter
                    continue
                
                if c.is_busy or c.cache.is_busy:
                    continue

                if c.has_instruction() == False:
                    done[c.core_num] = True
                    continue
                
                instr_type, data = c.execute_instruction()
                if instr_type == OTHER:
                    c.set_cycle_busy(data)
                    c.instruction_type[OTHER] += data
                
                if not snooping_busy:
                    c.cache.process_data(instr_type, data)
                    c.instruction_type[instr_type] += 1
                else:
                    c.stall_instruction()
            
            counter += 1
        end_time = time.time()
        self.time_taken = end_time - start_time                

    def results(self):
        pass



simulation = Simulation('mesi', 'blackscholes', 1024, 2, 16)
simulation.execute()
simulation.results()