import random

from Messages.Message import Message
from Util.Util import *
from Util.Forest import *


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
        self.public_block_forest = Forest(con=self.con,gamma=kargs["gamma"])
        self.private_block_forest = Forest(con=self.con,gamma=kargs["gamma"])
        self.private_chain_len = 0
        self.public_chain_len=0
        self.unpublished_len=0
        self.private_blocks=[]
        self.represent_id = self.con.n-1
    


    def receive_block(self):
        msgs = self.env.get_input_msg(self.chameleon_dict[self.represent_id])
        if not msgs:
            return
        for msg in msgs:
            block = msg.get_extraction()
            if not self.public_block_forest.block_is_in(block):
                self.public_block_forest.insert(block)
            self.private_chain_len=len(self.private_block_forest.get_chain())
            self.public_chain_len=len(self.public_block_forest.get_chain())
            if self.public_chain_len>self.private_chain_len:
                self.private_block_forest=self.public_block_forest.clone()
                pass
            else:
                if self.private_chain_len-self.public_chain_len==1:
                    for i in range(len(self.private_blocks)):
                        block = self.private_blocks.pop()
                        self.env.put_broadcast(self, self.represent_id, self.pki.sign(
                            self.chameleon_dict[self.represent_id], Message(self.represent_id, block, round)))
                    self.public_block_forest=self.private_block_forest.clone()
                    self.con.dispatch_honest_message()
                    self.con.throw_adv_message()
                elif self.private_chain_len-self.public_chain_len==0:
                    for i in range(len(self.private_blocks)):
                        block = self.private_blocks.pop()
                        self.env.put_broadcast(self, self.represent_id, self.pki.sign(
                            self.chameleon_dict[self.represent_id], Message(self.represent_id, block, round)))
                        if not self.public_block_forest.block_is_in(block):
                            self.public_block_forest.insert(block)
                    self.con.dispatch_honest_message()
                    self.con.throw_adv_message()
                else:
                    pass
    def throw_message(self):
        self.env.get_input_msg(self.chameleon_dict[self.represent_id])

                



    def mine_block(self):
        new_block = Nakamoto_Block(
            self.private_block_forest.query_max_depth_block_id(),miner=self.represent_id)
        self.private_blocks.append(new_block)
        self.env.insert_block(new_block)
        self.private_block_forest.insert(new_block)

    def put_output(self):
        self.env.put_output(self, ContentToString(
            self.private_block_forest.get_chain()))

       



            
                

        
        