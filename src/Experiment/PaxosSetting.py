from src.Controllers.PaxosController import *
from src.Environments.PaxosEnvironment import *
from src.Protocols.Paxos import *
from src.Protocols.FigPaxos import *
from src.Adversaries.PaxosDDOS import *


class PaxosSetting:

    def __init__(self, n, seed = None, protocol = Paxos, adv = None, measure = None):
        self.experiment_type = "Paxos Asynchronous"
        self.n = n
        self.con_type = PaxosController
        self.env_type = PaxosEnvironment
        self.protocol = protocol
        self.adv_type = adv
        self.seed = seed
        self.measure = measure

    def clone(self):
        raise NotImplementedError

    def report(self):
        pass

    def __str__(self):
        current_name = self.protocol.name
        return current_name

    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_n(self, n):
        self.n = n

    def set_seed(self, seed):
        self.seed = seed

    def get_protocol(self):
        return self.protocol
