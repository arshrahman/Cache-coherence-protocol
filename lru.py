class LRU:
    def __init__(self, associativity, set_index):
        self.associativity = associativity
        self.set_index = set_index
        self.blocks = []

    def reorder_to_recent(self, index):
        self.blocks.insert(0, self.blocks.pop(index))

    def cache_replacement(self, tag):
        removed_tag = -1
        if tag in self.blocks:
            self.reorder_to_recent(self.blocks.index(tag))
        elif len(self.blocks) == self.associativity:
            removed_tag = self.blocks.pop()
        
        self.blocks.insert(0, tag)
        return removed_tag

