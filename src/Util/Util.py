from Experiment.Experiment import *


def ContentToString(input):
    if type(input) is tuple:
        return '('+str(input[0])+','+(''.join(str(e) + ' ' for e in input[1]))[0:-1]+')'
    if type(input) is list:
        return (''.join(str(e) + ' ' for e in input))[0:-1]
    else:
        return str(input)


class Block:
    def __init__(self, round, id, belief):
        self.round = round
        self.id = id
        self.belief = belief

    def verify(self):
        return True

    def __str__(self):
        return str(self.round) + '-' + str(self.id) + '-' + str(self.belief)

    def get_sender(self):
        return self.id


class Nakamoto_Block:
    current_id = 1

    def __init__(self, previous_id, id=None):
        if id==None:
            self.id = Nakamoto_Block.current_id
            Nakamoto_Block.current_id += 1
            self.previous_id = previous_id
            
        else:
            self.id = id
            self.previous_id = previous_id

    @classmethod
    def get_genesis_block(self):
        local_current_id = Nakamoto_Block.current_id
        Nakamoto_Block.current_id = 0
        genesis_block = Nakamoto_Block(-1)
        Nakamoto_Block.current_id = local_current_id
        return genesis_block

    def check_is_previous(self, previous_id):
        return self.previous_id == previous_id

    def clone(self):
        return Nakamoto_Block(self.previous_id, self.id)

    def get_id(self):
        return self.id

    def get_previous_id(self):
        return self.previous_id

    def __str__(self):
        return str(self.previous_id)+'|'+str(self.id)

    def __eq__(self, other):
        return self.__key() == other.__key()
    
    def __hash__(self):
        return hash(self.__key())

    def __key(self):
        return (self.id,self.previous_id)
