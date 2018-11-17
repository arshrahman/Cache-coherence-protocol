from collections import defaultdict
from constants import INVALID, SHARED, MODIFIED, EXCLUSIVE

class Snooping:
    def __init__(self, caches):
        self.caches = caches
        self.shared_cache = defaultdict(set)
        self.exclusive_cache = {}
        self.data_traffic = 0
        self.bus_updates = 0
        self.invalidations = 0
        self.stall_cycle = 0
        self.add_caches()

    def add_caches(self):
        for cache in self.caches:
            cache.set_common_snooping(self)

    def add_shared_cache(self, core_num, block_index):
        self.shared_cache[block_index].add(core_num)
        self.exclusive_cache[block_index] = (len(self.shared_cache[block_index]) == 1)

    def remove_shared_cache(self, core_num, block_index):
        if block_index in self.shared_cache and core_num in self.shared_cache[block_index]:
            self.shared_cache[block_index].remove(core_num)
            self.exclusive_cache[block_index] = (len(self.shared_cache[block_index]) == 1)
            if (len(self.shared_cache[block_index]) == 0):
                self.shared_cache.pop(block_index)
                self.exclusive_cache.pop(block_index)                 
    
    def is_cache_shared(self, block_index):
        return (block_index in self.shared_cache)
    
    def is_cache_exclusive(self, block_index):
        return self.exclusive_cache.get(block_index, False)

    #Snooping gets busy when transfering a cache block from one processor to another
    def is_busy(self):
        if self.stall_cycle <= 1:
            self.stall_cycle = 0
            return False
        else:
            self.stall_cycle -= 1
            return True

    def set_cycle_busy(self, cycles):
        self.stall_cycle += cycles

    def snoop_caches(self, core_num, instr_type, snoop_action, block_index, set_index, tag):
        if snoop_action is None:
            return
        
        self.data_traffic += 1
        is_private_access = is_public_access = False
        for cache in self.caches:
            if cache.core_num == core_num:
                continue
            cache_state = cache.snooping_next_state_transtion(instr_type, snoop_action, block_index, set_index, tag)

            if cache_state == MODIFIED or cache_state == EXCLUSIVE:
                is_private_access = True
            elif cache_state == SHARED:
                is_public_access = True
        
        if is_private_access:
            self.caches[core_num].private_data_access += 1
        if is_public_access:
            self.caches[core_num].public_data_access += 1


