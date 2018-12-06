import copy
import itertools
import random

from Util.Util import *


class Forest:
    def __init__(self, _dict={}, max_depth_block_id=0,max_depth_block_miner=None, max_depth=1,gamma=1,con=None):
        if not _dict:
            self._dict = {}
            self._dict[0] = Nakamoto_Block(-1, has_genesis=True, id=0, depth=1)
            self.max_depth_block_id = 0
            self.max_depth_block_miner = None
            self.max_depth = 1
            self.gamma=gamma
            self.con = con
        else:
            self._dict = DictDeepCopy(_dict)
            self.max_depth_block_id = max_depth_block_id
            self.max_depth_block_miner = max_depth_block_miner
            self.max_depth = max_depth
            self.gamma=gamma
            self.con = con

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
            if block.id not in self._dict[block.previous_id].children_list:
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

    def update_depth(self, block, depth):
        block.depth = depth
        if not block.children_list:
            if self.max_depth < block.depth:
                self.max_depth = block.depth
                self.max_depth_block_id = block.id
                self.max_depth_block_miner = block.miner
                return
            elif self.max_depth > block.depth:
                return
            else:
                if self.con==None:
                    if block.id < self.max_depth_block_id:
                        self.max_depth = block.depth
                        self.max_depth_block_id = block.id
                        self.max_depth_block_miner = block.miner
                        return
                count=0
                if self.con.is_corrupt(block.miner):
                    count=count+1
                if self.con.is_corrupt(self.max_depth_block_miner):
                    count=count+1
                if count!=1:
                    if block.id < self.max_depth_block_id:
                        self.max_depth = block.depth
                        self.max_depth_block_id = block.id
                        self.max_depth_block_miner = block.miner
                        return
                else:
                    random_point = random.uniform(0,1)
                    if random_point <= self.gamma and self.con.is_corrupt(block.miner):
                        self.max_depth = block.depth
                        self.max_depth_block_id = block.id
                        self.max_depth_block_miner = block.miner
                        return
                    elif random_point > self.gamma and not self.con.is_corrupt(block.miner):
                        self.max_depth = block.depth
                        self.max_depth_block_id = block.id
                        self.max_depth_block_miner = block.miner
                        return
        for children in block.children_list:
            self._dict[children].has_genesis = True
            self.update_depth(self._dict[children],block.depth+1)
        

    # def update_depth(self, block, depth):
    #     block.depth = depth
    #     if not block.children_list:
    #         if self.max_depth < block.depth: 
    #             # or self.max_depth == block.depth and block.id < self.max_depth_block_id:
    #             self.max_depth = block.depth
    #             self.max_depth_block_id = block.id
    #         elif self.max_depth == block.depth:
    #             if random.randint(0,1)==1:
    #                 self.max_depth = block.depth
    #                 self.max_depth_block_id = block.id
    #         else:
    #             pass
    #     for children in block.children_list:
    #         self._dict[children].has_genesis = True
    #         self.update_depth(self._dict[children],block.depth+1)

    def clone(self):
        return Forest(self._dict, self.max_depth_block_id,self.max_depth_block_miner,self.max_depth,self.gamma,self.con)
    

