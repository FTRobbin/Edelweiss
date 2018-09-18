import random

from Messages.Message import Message
from Util.Util import *


class AsynNakamotoSelfishMiner:
    name = "Asynchronous Nakamoto selfish miner"

    def __init__(self, **kargs):
        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.con = kargs["con"]
        self.pki.register(self)
        self.called = 0
        self.corrupt_node_list = list(
            filter(lambda x: self.env.check_corrupt(x), range(self.env.get_n())))
        self.chameleon_dict = {}
        for node in self.con.node_id.keys():
            id = node.env.get_id(node)
            if self.env.check_corrupt(id):
                self.chameleon_dict[id] = node
        self.public_block_forest = Forest(Nakamoto_Block.get_genesis_block())
        self.private_block_forest = Forest(Nakamoto_Block.get_genesis_block())
        self.private_branch_len = 0
    def receive_block(self,id):
        msg = self.env.get_input_msg(self.chameleon_dict[id])
        if not msg:
            return
        block = msg.get_extraction()
        if self.public_block_forest.block_is_in(block):
            return
        delta_prev=len(self.private_block_forest.get_longest_chain())-len(self.public_block_forest.get_longest_chain())
        self.public_block_forest.insert(block)
        if delta_prev==0:
            
        
        