from constants import MESI, DRAGON, WRONG_COMMAND, TOTAL_CORES, LOAD, STORE, OTHER_INSTRUCTION, COUNT
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
        print('simulating...')
        self.counter = 1
        done = [False for i in range(TOTAL_CORES)]
        start_time = time.time()

        while not all(done):
            snooping_busy = self.snooping.is_busy()
            for c in self.cores:
                #print('core num', c.core_num, 'instuction num: ', c.current_instruction, ' core cycle ', c.stall_cycle, ' cache cycle ', c.cache.stall_cycle, 'snoop cycle ', self.snooping.stall_cycle)
                if done[c.core_num]:
                    c.instruction_type[COUNT] = self.counter if c.instruction_type[COUNT] == 0 else c.instruction_type[COUNT]
                    continue
                
                if c.is_busy() or c.cache.is_busy():
                    continue

                if c.has_instruction() == False:
                    done[c.core_num] = True
                    continue
                
                instr_type, data = c.execute_instruction()
                if instr_type == OTHER_INSTRUCTION:
                    c.set_cycle_busy(data)
                    c.instruction_type[OTHER_INSTRUCTION] += data
                    continue
                
                if not snooping_busy or not c.cache.is_generate_bus(instr_type, data):
                    has_scheduled_update = c.cache.process_data(instr_type, data)
                    if has_scheduled_update:
                        c.stall_instruction()
                    else:
                        c.instruction_type[instr_type] += 1
                else:
                    c.stall_instruction()
            
            self.counter += 1
        
        end_time = time.time()
        self.time_taken = end_time - start_time                

    def results(self):
        print('SIMULATION REPORT')
        print('------------------------------')
        
        print('Time taken:', self.time_taken)
        print('Overall Execution Cycle:', self.counter, '\n')
        
        print('Bus snooping results')
        print('Data traffic:', self.snooping.data_traffic, '|',  
            'Invalidations:', self.snooping.invalidations, '|',  'Bus updates:', self.snooping.bus_updates, '\n');
        print('------------------------------')
        # print('Data traffic:', self.snooping.data_traffic)
        # print('Invalidations: ', self.snooping.invalidations)
        # print('Bus updates: ', self.snooping.bus_updates, '\n')

        for i in range(TOTAL_CORES):
            total_cycles = self.cores[i].instruction_type[COUNT] if self.cores[i].instruction_type[COUNT] > 0 else self.counter
            total_data_instr = self.cores[i].instruction_type[LOAD] + self.cores[i].instruction_type[STORE]
            data_miss_rate =  (100.0  * (self.caches[i].data_miss / total_data_instr)) if total_data_instr > 0 else 0.0

            print('Core', i, '|', 'Total cycles:', total_cycles, '|', 'Compute cycles:', self.cores[i].instruction_type[OTHER_INSTRUCTION], '|',
                'Load cycles:', self.cores[i].instruction_type[LOAD], '|', 'Store cycles:', self.cores[i].instruction_type[STORE], '|', 
                'Idle cycles:', self.caches[i].idle_cycles, '|', 'Data miss rate:', data_miss_rate, '|', 'Private data accesses:', self.caches[i].private_data_access,
                '|', 'Public data accesses:', self.caches[i].public_data_access)
            print('------------------------------')
            # print('Total cycles: ', total_cycles)
            # print('Compute cycles: ', self.cores[i].instruction_type[OTHER_INSTRUCTION])
            # print('Load cycles: ', self.cores[i].instruction_type[LOAD])
            # print('Store cycles: ', self.cores[i].instruction_type[STORE])
            # print('Idle cycles: ', self.caches[i].idle_cycles)
            # print('Data miss rate: ', data_miss_rate)
            # print('Private data accesses: ', self.caches[i].private_data_access)
            # print('Public data accesses: ', self.caches[i].public_data_access, '\n')

#simulation = Simulation('dragon', 'blackscholes', 1024, 2, 16)
#simulation.execute()
#simulation.results()

#simulation = Simulation('mesi', 'blackscholes', 1024, 2, 16)
#simulation.execute()
#simulation.results()