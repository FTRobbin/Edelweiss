from Controllers.SynController import *
from Environments.SynEnvironment import *
from Environments.AsynEnvironment import *
from Oracles.PKI import *
from Adversaries import *


class AsynchronousByzantine:
    def __init__(self, n, input, adversary, controller,
                 f=0, tf=0,
                 protocol=None, measure=[],
                 centralized=False, centralized_adversary=None,
                 has_sender=False, corrupt_sender=False, seed=None, _lambda=-1, k=1):
        self.experiment_type = "Asynchronous Byzantine"
        self.n = n
        self.input = input
        self.f = f
        self.tf = tf
        self.adversary = adversary
        self.con_type = controller
        self.env_type = AsynEnvironment
        self.pki_type = IdealPKI
        self.protocol = protocol
        self.centralized = centralized
        self.centralized_adversary = centralized_adversary
        self.measure = measure
        self.has_sender = has_sender
        self.corrupt_sender = corrupt_sender
        self.seed = seed
        self._lambda = _lambda
        self.k = k

    def clone(self):
        raise NotImplementedError

    def report(self):
        raise NotImplementedError

    def __str__(self):
        current_name = self.protocol.name+str(self.input)+str(self.centralized)
        if self.tf > 0:
            if self.centralized:
                current_name += self.centralized_adversary.name+self.f+self.tf
            else:
                current_name += self.adversary.name+str(self.f)+str(self.tf)
        return current_name

    def set_input(self, input):
        self.input = input

    def get_input(self):
        return self.input

    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_adversary(self, adversary):
        self.adversary = adversary

    def get_adversary(self):
        return self.adversary.name

    def set_centralized_adversary(self, centralized_adversary):
        self.centralized_adversary = centralized_adversary

    def get_centralized_adversary(self):
        return self.centralized_adversary.name

    def set_n(self, n):
        self.n = n

    def set_f(self, f):
        self.f = f

    def set_tf(self, tf):
        self.tf = tf

    def set_seed(self, seed):
        self.seed = seed

    def set_lambda(self, _lambda):
        self._lambda = _lambda

    def set_k(self, k):
        self.k = k

    def get_protocol(self):
        return self.protocol

    def set_centralized(self, centralized):
        self.centralized = centralized

    def get_centralized(self):
        return self.centralized
