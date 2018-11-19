from constants import LOAD, STORE, READ, WRITE, COPY, MODIFIED, EXCLUSIVE, SHARED, INVALID, INSTRUCTION_MAP, MESI_STATE_MACHINE
from cache import Cache

class Mesi(Cache):
    def __init__(self, cache_size, associativity, block_size, core_num):
        Cache.__init__(self, cache_size, associativity, block_size, core_num)
        self.cache_transfer = (self.block_size // 4) * 2
        self.snoop_transaction = True

    def process_data(self, instr_type, data_address):
        _, set_index, tag = self.get_cache_info(data_address)
        block_index = self.get_block_index(set_index, tag)
        cache_state = self.cache_states[set_index]
        current_state = cache_state.setdefault(tag, INVALID)
        self.snoop_transaction = True
        new_state, snoop_action, stall_cycles = self.next_state_transition(current_state, instr_type, block_index)

        if self.has_scheduled_update:
            self.update_cache(cache_state, new_state, block_index, set_index, tag)
        else:
            self.schedule_update(cache_state, current_state, new_state, stall_cycles, block_index, set_index, tag)

        #print('core', self.core_num, 'instr_type', instr_type, 'snoop_action', snoop_action, 'next_state', new_state, 'set_index', set_index, 'tag', tag)
        if self.snoop_transaction and snoop_action is not None:
            self.snooping.snoop_caches(self.core_num, instr_type, snoop_action, block_index, set_index, tag)    
        return self.has_scheduled_update
    
    def next_state_transition(self, current_state, instr_type, block_index):
        if instr_type == LOAD and current_state == INVALID and self.snooping.is_cache_shared(block_index):
            return MESI_STATE_MACHINE[current_state][COPY]
        elif instr_type == LOAD:
            return MESI_STATE_MACHINE[current_state][READ]
        else:
            return MESI_STATE_MACHINE[current_state][WRITE]

    def is_cache_miss(self, state):
        return (state == INVALID)

    def update_cache(self, cache_state, new_state, block_index, set_index, tag):
        self.has_scheduled_update = False
        cache_state[tag] = new_state
        self.snooping.add_shared_cache(block_index, self.core_num) 

        removed_tag = self.cache_data[set_index].cache_replacement(tag)
        if removed_tag is not None:
            if cache_state[removed_tag] == MODIFIED:
                self.set_cycle_busy(100)
            self.cache_states[set_index].pop(removed_tag)
            removed_block_index = self.get_block_index(set_index, removed_tag)
            self.snooping.remove_shared_cache(removed_block_index, self.core_num)

    
    def schedule_update(self, cache_state, current_state, new_state, stall_cycles, block_index, set_index, tag):
        #check if cache is exclusive or modified in other cores
        if self.snooping.is_cache_exclusive(block_index) and current_state == INVALID:
            self.snooping.bus_updates += 1
            self.snooping.set_cycle_busy(self.cache_transfer)
            self.idle_cycles += self.cache_transfer
            self.data_miss += 1
            self.has_scheduled_update = True
            self.snoop_transaction = False
        else:
            if stall_cycles > 0:
                self.set_cycle_busy(stall_cycles)
                self.data_miss += 1
                self.has_scheduled_update = True
                self.snoop_transaction = False
            else:
                self.cache_hit(cache_state, new_state, set_index, tag)
    
    def cache_hit(self, cache_state, new_state, set_index, tag):
        self.cache_data[set_index].cache_replacement(tag) 
        cache_state[tag] = new_state

    def snooping_next_state_transtion(self, instr_type, snoop_action, block_index, set_index, tag):
        cache_state = self.cache_states[set_index]
        if tag in cache_state and cache_state[tag] != INVALID: 
            current_state = cache_state[tag]          
            new_state, _, stall_cycles = MESI_STATE_MACHINE[current_state][snoop_action]
            if new_state == INVALID:
                self.snooping.invalidations += 1
                self.snooping.remove_shared_cache(block_index, self.core_num)
            
            cache_state[tag] = new_state
            self.set_cycle_busy(stall_cycles)
            return current_state
        return INVALID
    
    def is_generate_bus(self, instr_type, data_address):
        _, set_index, tag = self.get_cache_info(data_address)
        current_state = INVALID if tag not in self.cache_states[set_index] else self.cache_states[set_index][tag]
        return current_state == INVALID or (current_state == SHARED and INSTRUCTION_MAP[instr_type] == STORE)
        



