import random
import itertools


class Forest:
    def __init__(self, genesis_block):
        self._dict = {}
        self._dict[genesis_block.id] = genesis_block.clone()
        self.max_depth_block_id = genesis_block.id
        self.max_depth = 1
    
    def block_is_in(self, block):
        return block.id in self._dict.keys() and self._dict[block.id].has_block

    def insert(self, block):
        if block.id in self._dict.keys():
            if self._dict[block.id].has_block:
                return
            else:
                self._dict[block.id].has_block = True
                self._dict[block.id].previous_id = block.previous_id
        else:
            # insert the block
            self._dict[block.id] = block.clone()
            self._dict[block.id].has_block = True
            self._dict[block.id].children_list = []
            self._dict[block.id].has_genesis = False
        # build the connection
        if block.previous_id in self._dict.keys():
            self._dict[block.previous_id].children_list.append(block.id)
            self._dict[block.id].has_genesis = self._dict[block.previous_id].has_genesis
            if self._dict[block.id].has_genesis:
                self.update_depth(self._dict[block.id],
                    self._dict[block.previous_id].depth+1)
        else:
            ghost_block = block.get_ghost_block(block.previous_id, block.id)
            self._dict[block.previous_id] = ghost_block

    def query_max_depth_block_id(self):
        return self.max_depth_block_id

    def get_chain(self):
        chain = []
        local_block_id = self.max_depth_block_id
        while local_block_id != 0:
            local_block = self._dict[local_block_id]
            chain.append(local_block)
            local_block_id = local_block.previous_id
        chain.append(self._dict[0])
        chain.reverse()
        return chain
        
    def update_depth(self,block,depth):
        block.depth = depth
        if not block.children_list:
            if self.max_depth < block.depth or self.max_depth == block.depth and block.id < self.max_depth_block_id:
                self.max_depth = block.depth
                self.max_depth_block_id = block.id
        for children in block.children_list:
            self._dict[children].has_genesis = True
            self._dict[children].update_depth(block.depth+1, self)
        

    def copy(self):
        pass



