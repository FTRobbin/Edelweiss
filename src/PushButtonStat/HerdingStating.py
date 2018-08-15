from Stat.Stat import *
from Test.TestConfig import *
from Protocols.HerdingWithBroadcastFast import *
from Protocols.HerdingWithBroadcast import *

# set parameter


def HerdingStating(h, input, times, _lambda_list, k_list, protocol_list, adversary_list, f_list):
    # Basic Herding with SynHerdingCentralizedValidity Attacker
    setting = SynchronousByzantine(None, None, None,
                                   PossibleControllers[0], f=None, tf=None, protocol=None,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=None, centralized_adversary=None, seed=None, _lambda=None, k=None)
    for protocol in protocol_list:
        for adversary in adversary_list:
            for _lambda in _lambda_list:
                for k in k_list:
                    for f in f_list:
                        tf = f
                        SetStatParaAndRun(
                            h, setting, input, times, f, tf, protocol, adversary, _lambda, k)
                        print(" ", file=h)
def CustomizedHerdingStating(h,para_setting_list):
    setting = SynchronousByzantine(None, None, None,
                                   PossibleControllers[0], f=None, tf=None, protocol=None,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=None, centralized_adversary=None, seed=None, _lambda=None, k=None)
    for para_setting in para_setting_list:
        SetStatParaAndRun(
                            h, setting, para_setting[0], para_setting[1], para_setting[2], para_setting[3], para_setting[4], para_setting[5], para_setting[6], para_setting[7])
        print(" ", file=h)

def HerdingStatingAll(times=1):
    h = open("HerdingStating.txt", "w+")
    input = 50*[1]+50*[0]
    # Experiment 1: Broken without broadcast
    protocol_list = [Herding]
    adversary_list = [PossibleAdversaries[5]]
    _lambda_list = [2]
    k_list = [5, 10, 15, 20, 25, 30]
    f_list = [20]
    HerdingStating(h, input, times, _lambda_list, k_list, protocol_list, adversary_list, f_list)
    # Experiment 2: Round, F, Bruteforce
    # Experiment 3: Round, F, Advanced
    protocol_list = [HerdingWithBroadcastFast]
    adversary_list = [PossibleAdversaries[6], PossibleAdversaries[7]]
    _lambda_list = [2]
    f_list = [20, 25, 30, 35, 40, 45, 50, 55, 60]
    HerdingStating(h, input, times, _lambda_list, k_list, protocol_list, adversary_list, f_list)
    # Experiment 4: Lambda
    # _lambda_list=[3,4,5]
    # para_setting_list=[]
    # for _lambda in _lambda_list:
    #     for f in f_list:
    #         k=int(100/(_lambda*_lambda))
    #         tf=f
    #         # h, setting, input, times, f, tf, protocol, adversary, _lambda, k)
    #         para_setting=(input,times,f,tf,HerdingWithBroadcastFast,PossibleAdversaries[7],_lambda,k)
    #         para_setting_list.append(para_setting)
    # CustomizedHerdingStating(h,para_setting_list)
    h.close()
