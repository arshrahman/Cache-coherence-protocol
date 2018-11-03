from lru import LRU

class Cache:
    def __init__(self, cache_size, associativity, block_size, core_num):
        self.associativity = associativity
        self.block_size = block_size
        self.core_num = core_num
        self.set_size = cache_size // (associativity * block_size) 
        self.cache_states = [{} for i in range(self.set_size)]
        self.cache_sets = [LRU(associativity, i) for i in range(self.set_size)]

