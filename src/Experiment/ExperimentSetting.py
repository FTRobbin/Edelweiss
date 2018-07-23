from Controllers.Controller import *
from Environments.Environment import *
from Oracles.PKI import *


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
