from Controllers.SynByzController import *
from Controllers.SynByzController import *
from Environments.Environment import *
from Oracles.PKI import *
from Adversaries import *


class ExperimentSetting:
    def __init__(self):
        # TODO
        pass


class SynchronousByzantine:
    def __init__(self, n, input, adversary, controller,
                 f=0, tf=0,
                 protocol=None, measure=[],
                 centralized=False, centralized_adversary=None,
                 has_sender=False, corrupt_sender=False):
        self.experiment_type = "Synchronous Byzantine"
        self.n = n
        self.input = input
        self.f = f
        self.tf = tf
        self.adversary = adversary
        self.con_type = controller
        self.env_type = SynByzEnvironment
        self.pki_type = IdealPKI
        self.protocol = protocol
        self.measure = measure
        self.centralized = centralized
        self.centralized_adversary = centralized_adversary
        self.has_sender = has_sender
        self.corrupt_sender = corrupt_sender

    def clone(self):
        ret = SynchronousByzantine(
            self.n, self.input, self.f, self.corrupt_sender, self.protocol, self.measure)
        ret.adversary = self.adversary
        return ret

    def report(self):
        tf = self.f
        print("Synchronous Byzantine")
        print("Controller : " + self.con_type.name)
        print("Environment : " + self.env_type.name)
        print("PKI : " + self.pki_type.name)
        print("Protocol : " + self.protocol.name)
        if tf > 0:
            print("Adversary : " + self.adversary.name)
        print("")
        print("Parameters:")
        print("n : %d" % self.n)
        if (type(self.input) is list):
            for i in range(self.n):
                print("input : %d" % self.input[i])
        else:
            print("input : %d" % self.input)
        if tf > 0:
            print("num of corruptions : %d" % tf)
