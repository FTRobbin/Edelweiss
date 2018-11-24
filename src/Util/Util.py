import socket

def isListEmpty(inList):
    if isinstance(inList, list):  # Is a list
        return all(map(isListEmpty, inList))
    return False  # Not a list


def DictDeepCopy(dict_input):
    _dict = {}
    for k, v in dict_input.items():
        _dict[k] = v.clone()
    return _dict


def ContentToString(input):
    if type(input) is tuple:
        return '('+str(input[0])+','+(''.join(str(e) + ' ' for e in input[1]))[0:-1]+')'
    if type(input) is list:
        return (''.join(str(e) + ' ' for e in input))[0:-1]
    else:
        return str(input)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip




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

    def __init__(self, previous_id, has_block=True, children_list=[], has_genesis=False, id=None, depth=None, miner=None):
        if id == None:
            self.id = Nakamoto_Block.current_id
            Nakamoto_Block.current_id += 1
            self.previous_id = previous_id
            self.has_block = has_block
            self.children_list = children_list
            self.has_genesis = has_genesis
            self.depth = depth
            self.miner = miner
        else:
            self.id = id
            self.previous_id = previous_id
            self.has_block = has_block
            self.children_list = children_list
            self.has_genesis = has_genesis
            self.depth = depth
            self.miner = miner

    @staticmethod
    def get_genesis_block():
        genesis_block = Nakamoto_Block(-1, has_genesis=True, id=0, depth=1)
        return genesis_block

    def get_ghost_block(self, ghost_id, child_id):
        ghost_block = Nakamoto_Block(None, has_block=False, children_list=[
                                     child_id], has_genesis=None, id=ghost_id)
        return ghost_block

    def clone(self):
        return Nakamoto_Block(self.previous_id, self.has_block, self.children_list.copy(), self.has_genesis, self.id, self.depth, self.miner)

    def __copy__(self):
        return self.clone()

    def __str__(self):
        return str(self.previous_id)+'|'+str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.__key())

    def __key(self):
        return (self.id, self.previous_id)

    def get_miner(self):
        return self.miner
    
        
