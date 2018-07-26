from Controllers.Controller import *
from Environments.Environment import *
from Oracles.PKI import *
from Adversaries.Adversary import *


class ExperimentSetting:
    def __init__(self):
        # TODO
        pass


class SynchronousByzantine:
    def __init__(self, n, input, f=0, corflag=False, protocol=None, measure=[]):
        self.n = n
        self.input = input
        self.f = f
        self.corrupt_sender = corflag
        self.adversary = None
        self.con_type = SynByzController
        self.env_type = SynByzEnvironment
        self.pki_type = IdealPKI
        self.protocol = protocol
        self.measure = measure

    def clone(self):
        ret = SynchronousByzantine(self.n, self.input, self.f, self.corrupt_sender, self.protocol, self.measure)
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
        print("input : %d" % self.input)
        if tf > 0:
            print("num of corruptions : %d" % tf)
            print("sender corrupted : %s" % str(self.corrupt_sender))


class SynchronousByzantineWithoutSender:
    def __init__(self, n, input, adversary, controller,
                 f=0, tf=0,
                 protocol=None, measure=[]):
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

    def clone(self):
        ret = SynchronousByzantine(self.n, self.input, self.f, self.corrupt_sender, self.protocol, self.measure)
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
        for i in range(self.n):
            print("input : %d" % self.input[i])
        if tf > 0:
            print("num of corruptions : %d" % tf)
