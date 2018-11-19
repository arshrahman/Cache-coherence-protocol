
from constants import LOAD, STORE, READ, WRITE, WRITE_UPDATE, COPY, BUS_READ, BUS_UPDATE, MODIFIED, EXCLUSIVE, SHARED, SHARED_CLEAN, SHARED_MODIFIED, INVALID, INSTRUCTION_MAP, DRAGON_STATE_MACHINE
from cache import Cache

class Dragon(Cache):
    def __init__(self, cache_size, associativity, block_size, core_num):
        Cache.__init__(self, cache_size, associativity, block_size, core_num)
        self.cache_transfer_cycle = 2
        self.scheduled_block_index = -1
        self.cache_to_cache_transfer = False

    
    def process_data(self, instr_type, data_address):
        _, set_index, tag = self.get_cache_info(data_address)
        block_index = self.get_block_index(set_index, tag)
        cache_state = self.cache_states[set_index]
        current_state = INVALID if tag not in cache_state else cache_state[tag]
        cache_shared = self.snooping.is_cache_shared(block_index)
        snoop_transaction = True
        
        state_transition = self.get_next_state(instr_type, current_state, cache_shared)
        next_state, snoop_action, stall_cycles = DRAGON_STATE_MACHINE[current_state][state_transition]
        
        if self.has_scheduled_update:
            self.update_cache(cache_state, next_state, block_index, set_index, tag)
            snoop_transaction = not self.cache_to_cache_transfer
            self.cache_to_cache_transfer = False
        else:
            if current_state == INVALID:
                self.schedule_update(cache_shared, stall_cycles, block_index)
            else:
                self.cache_hit(cache_state, next_state, set_index, tag)
        
        if snoop_transaction and snoop_action is not None:
            self.snooping.snoop_caches(self.core_num, instr_type, snoop_action, block_index, set_index, tag)    
            if snoop_action == BUS_UPDATE or (snoop_action == BUS_READ and cache_shared and current_state == INVALID):
                self.snooping.bus_updates += 1

        return self.has_scheduled_update

    def get_next_state(self, instr_type, current_state, cache_shared):
        if current_state == INVALID:
            if cache_shared:
                return COPY if instr_type == LOAD else WRITE_UPDATE
            else:
                return READ if instr_type == LOAD else WRITE
        elif current_state == SHARED_CLEAN or current_state == SHARED_MODIFIED:
            if cache_shared:
                return WRITE_UPDATE if instr_type == STORE else READ
            else:
                return WRITE if instr_type == STORE else READ
        elif current_state == MODIFIED or current_state == EXCLUSIVE:
            return WRITE if instr_type == STORE else READ
    
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
    
    def schedule_update(self, cache_shared, stall_cycles, block_index):
        self.has_scheduled_update = True
        self.data_miss += 1

        if cache_shared:
            self.set_cycle_busy(self.cache_transfer_cycle)
            self.cache_to_cache_transfer = True
        else: 
            self.scheduled_block_index = block_index
            self.set_cycle_busy(stall_cycles)
    
    def cache_hit(self, cache_state, new_state, set_index, tag):
        self.cache_data[set_index].cache_replacement(tag) 
        cache_state[tag] = new_state
  
    def snooping_next_state_transtion(self, instr_type, snoop_action, block_index, set_index, tag):
        cache_state = self.cache_states[set_index]
        if tag in cache_state: 
            current_state = cache_state[tag]
            if snoop_action == BUS_UPDATE and (current_state == MODIFIED or current_state == EXCLUSIVE):
                return current_state

            next_state, _, _ = DRAGON_STATE_MACHINE[current_state][snoop_action]
            cache_state[tag] = next_state

            if snoop_action == BUS_UPDATE:
                self.set_cycle_busy(self.cache_transfer_cycle)
                self.snooping.set_cycle_busy(self.cache_transfer_cycle)
            elif snoop_action == BUS_READ:
                if self.has_scheduled_update and self.scheduled_block_index == block_index:
                    self.has_scheduled_update = False
                    self.scheduled_block_index = -1
                    self.set_cycle_busy(self.cache_transfer_cycle)
                
                self.snooping.set_cycle_busy(self.cache_transfer_cycle)
            self.idle_cycles += self.cache_transfer_cycle
            
            return current_state
        return INVALID   


    def is_generate_bus(self, instr_type, data_address):
        _, set_index, tag = self.get_cache_info(data_address)
        current_state = INVALID if tag not in self.cache_states[set_index] else self.cache_states[set_index][tag]
        return current_state == INVALID or ((current_state == SHARED_CLEAN or current_state == SHARED_MODIFIED) and INSTRUCTION_MAP[instr_type] == STORE)