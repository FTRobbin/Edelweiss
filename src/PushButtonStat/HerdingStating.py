from Stat.Stat import *
from Test.TestConfig import *

# set parameter


def HerdingStating():
    # Basic Herding with SynHerdingCentralizedValidity Attacker
    h = open("HerdingStating.txt", "w+")
    setting = SynchronousByzantine(None, None, None,
                                   PossibleControllers[0], f=None, tf=None, protocol=None,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=None, centralized_adversary=None, seed=None, _lambda=None, k=None)
    input = 50*[1]+50*[0]
    times = 1000
    _lambda_list = [4]
    k_list = [4, 8, 16]
    protocol_list = [Herding,HerdingWithBroadcast]
    adversary_list = [PossibleAdversaries[5],PossibleAdversaries[6]]
    f_list = [27,33,38,44,50,55]
    for protocol in protocol_list:
        for adversary in adversary_list:
            for _lambda in _lambda_list:
                for k in k_list:
                    for f in f_list:
                        tf = f
                        SetStatParaAndRun(
                            h, setting, input, times, f, tf, protocol, adversary, _lambda, k)
                        print(" ", file=h)
    h.close()
