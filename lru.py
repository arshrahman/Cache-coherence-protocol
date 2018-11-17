class LRU:
    def __init__(self, associativity, set_index):
        self.associativity = associativity
        self.set_index = set_index
        self.blocks = []

    def reorder_to_recent(self, index):
        popped = self.blocks.pop(index)
        self.blocks.insert(0, popped)

    def cache_replacement(self, tag):
        removed_tag = None
        if tag in self.blocks:
            block_index = self.blocks.index(tag)
            self.reorder_to_recent(block_index)
        else:
            if len(self.blocks) == self.associativity:
                removed_tag = self.blocks.pop()
            self.blocks.insert(0, tag)
        return removed_tag

