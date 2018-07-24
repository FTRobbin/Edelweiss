from Controllers.Controller import *
from Environments.Environment import *
from Oracles.PKI import *
from Adversaries.Adversary import *


class ExperimentSetting:
    def __init__(self):
        # TODO
        pass


class SynchronousByzantine:
    def __init__(self, n, input, protocol,
                 adv_class=None, adv_para=None,
                 measure=None):
        self.n = n
        self.input = input
        self.protocol = protocol
        self.adv_class = adv_class
        self.adv_para = adv_para
        self.con_class = SynByzController
        self.env_class = SynByzEnvironment
        self.pki_class = IdealPKI
        if measure is not None:
            self.measure = measure
        else:
            self.measure = []

    def clone(self):
        return SynchronousByzantine(self.n, self.input, self.protocol,
                                    self.adv_class, self.adv_para,
                                    self.measure[:])

    def report(self):
        print("Experiment Setting:")
        print("Synchronous Byzantine")
        print("Controller : " + self.con_class.name)
        print("Environment : " + self.env_class.name)
        print("PKI : " + self.pki_class.name)
        print("Protocol : " + self.protocol.name)
        if self.adv_class is not None:
            print("Adversary : " + self.adv_class.name)
            print("")
            print("Parameters:")
            print("n : %d" % self.n)
            print("input : %d" % self.input)
            self.adv_class.report_parameters(self.adv_para)
        else:
            print("")
            print("Parameters:")
            print("n : %d" % self.n)
            print("input : %d" % self.input)
        print("")
<<<<<<< HEAD
        print("Parameters:")
        print("n : %d" % self.n)
        print("input : %d" % self.input)
        if tf > 0:
            print("num of corruptions : %d" % tf)
            print("sender corrupted : %s" % str(self.corrupt_sender))

class SynchronousByzantineWithoutSender:
    def __init__(self, n, input, f=0, protocol=None, measure=[]):
        self.n = n
        self.input = input
        self.f = f
        self.adversary = CrashAdversary
        self.con_type = SynByzControllerWithoutSender
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

class AsynchronousByzantine:
    def __init__(self, n, input, f=0, corflag=False, protocol=None, measure=[]):
        self.n = n
        self.input = input
        self.f = f
        self.corrupt_sender = corflag
        self.adversary = None
        self.con_type = AsynByzController
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

=======
>>>>>>> 7a1ca05d6a6fdee0570ebb4de48d0a256ef8ed7d
