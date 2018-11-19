from collections import defaultdict
from lru import LRU

class Cache:
    def __init__(self, cache_size, associativity, block_size, core_num):
        self.associativity = associativity
        self.block_size = block_size
        self.core_num = core_num
        self.set_size = cache_size // (associativity * block_size) 
        self.cache_states = defaultdict(dict)
        self.cache_data = [LRU(associativity, i) for i in range(self.set_size)]
        self.has_scheduled_update = False
        self.stall_cycle = 0
        self.private_data_access = 0
        self.public_data_access = 0
        self.idle_cycles = 0
        self.data_miss = 0

    def set_common_snooping(self, snooping):
        self.snooping = snooping 
    
    #cache gets busy when transfering of data between cache and main memory
    def is_busy(self):
        if self.stall_cycle <= 1:
            self.idle_cycles += self.stall_cycle
            self.stall_cycle = 0 
            return False
        else:
            self.stall_cycle -= 1
            self.idle_cycles += 1
            return True

    def set_cycle_busy(self, cycles):
        self.stall_cycle = cycles

    def get_cache_info(self, data_address):
        block_index = data_address // self.block_size
        set_index = block_index % self.set_size
        tag = block_index // self.set_size
        return block_index, set_index, tag
    
    def get_block_index(self, set_index, tag):
        return (tag * self.set_size + set_index) * self.block_size