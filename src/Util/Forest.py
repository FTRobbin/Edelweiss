import random
import itertools


class Forest:
    def __init__(self, genesis_block):
        self.dict = {}
        self.dict[genesis_block.id] = genesis_block.clone()
        self.max_depth_block_id = genesis_block.id
        self.max_depth = 1

    def block_is_in(self, block):
        return block.id in self.dict.keys() and self.dict[block.id].has_block

    def insert(self, block):
        if block.id in self.dict.keys():
            if self.dict[block.id].has_block:
                return
            else:
                self.dict[block.id].has_block = True
                self.dict[block.id].previous_id = block.previous_id
        else:
            # insert the block
            self.dict[block.id] = block.clone()
            self.dict[block.id].has_block = True
            self.dict[block.id].children_list = []
            self.dict[block.id].has_genesis = False
        # build the connection
        if block.previous_id in self.dict.keys():
            self.dict[block.previous_id].children_list.append(block.id)
            self.dict[block.id].has_genesis = self.dict[block.previous_id].has_genesis
            if self.dict[block.id].has_genesis:
                self.dict[block.id].update_depth(
                    self.dict[block.previous_id].depth+1, self)
        else:
            ghost_block = block.get_ghost_block(block.previous_id, block.id)
            self.dict[block.previous_id] = ghost_block

    def query_max_depth_block_id(self):
        return self.max_depth_block_id

    def get_chain(self):
        chain = []
        local_block_id = self.max_depth_block_id
        while local_block_id != 0:
            local_block = self.dict[local_block_id]
            chain.append(local_block)
            local_block_id = local_block.previous_id
        chain.append(self.dict[0])
        chain.reverse()
        return chain
