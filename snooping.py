from collections import defaultdict

class Snooping:
    def __init__(self, caches):
        self.caches = caches
        self.shared_cache = defaultdict(set)
        self.exclusive_cache = {}
        self.data_traffic = 0
        self.bus_updates = 0
        self.invalidations = 0
        self.caches.snooping = self

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




