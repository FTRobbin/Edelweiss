# from Experiment.Experiment import *


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


class Tangle_Site:
    current_id = 2

    def __init__(self, father_id_list, children_list, miner, id=None):
        if id == None:
            self.id = Tangle_Site.current_id
            Tangle_Site.current_id = Tangle_Site.current_id+1
            self.father_id_list = father_id_list
            self.children_list = children_list
            self.miner = miner
        else:
            self.id = id
            self.father_id_list = father_id_list
            self.children_list = children_list
            self.miner = miner

    @staticmethod
    def get_genesis_site():
        genesis_site = Tangle_Site([], [], None, 1)
        return genesis_site

    def calculate_cumulative_weight(self):
        len(self.calculate_descendants())
        return len(self.calculate_descendants())

    def calculate_descendants(self):
        descendant_set = set()
        descendant_set.add(self.id)
        if not self.children_list:
            return {self}
        for child in self.children_list:
            descendant_set = descendant_set.union(
                child.calculate_descendants())
        return descendant_set

    def find_site_with_id(self, id):
        site = None
        if self.id == id:
            site = self
            return site
        if not self.children_list:
            return site
        for child in self.children_list:
            site = child.find_site_with_id(id)
            if site:
                return site
        return site
    def clone(self):
        return Tangle_Site(self.father_id_list.copy(), [], self.miner, self.id)

    def copy(self):
        return self.clone()
    
    def check_site_present(self,site):
        if self.id==site.id:
            return True
        if not self.children_list:
            return False
        for child in self.children_list:
            if child.check_site_present(site):
                return True
        return False

    def check_identical_site(self, another_site):
        if self.id != another_site.id:
            return False
        if self.father_id_list != another_site.father_id_list:
            return False
        if not self.children_list:
            if not another_site.children_list:
                return True
            return False
        mychildren_dict = {}
        for child in self.children_list:
            mychildren_dict[child.id] = child
        hischildren_dict = {}
        for child in another_site.children_list:
            hischildren_dict[child.id] = child
        if len(mychildren_dict) != len(hischildren_dict):
            return False
        for k, v in mychildren_dict.items():
            if k not in hischildren_dict.keys():
                return False
            if not v.check_identical_site(hischildren_dict[k]):
                return False
        return True

    def get_sender(self):
        return self.miner
    
        
