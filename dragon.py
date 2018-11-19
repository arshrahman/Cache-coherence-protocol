from cache import Cache

class Dragon(Cache):
    def __init__(self, cache_size, associativity, block_size, core_num):
        Cache.__init__(self, cache_size, associativity, block_size, core_num)