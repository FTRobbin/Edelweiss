import random

from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Test.Report import *
from test import *
from Stat.AdversaryStat import *
from Stat.Stat import *
from Protocols.HerdingWithBroadcast import *
from Adversaries.SynHerdingBenchmarkAttacker import *
def SynHerdingValidityAttackStat(input,times,k,_lambda_loacl,f_list,protocol_local,adversary_local):
    setting = SynchronousByzantine(100, input, adversary_local,
                                   PossibleControllers[0], f=0, tf=0, protocol=protocol_local,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=True, centralized_adversary=adversary_local, seed=None, _lambda=_lambda_loacl,k=1)
    print("protocol="+setting.get_protocol().name)
    print("adversary="+setting.get_centralized_adversary().name)
    print("times="+str(times))
    print("k="+str(k))
    print("lambda="+str(_lambda_loacl))
    for f in f_list:
        print("f="+str(f))
        tf=f
        stat(setting,input,f,tf,_lambda_loacl,times) # atomtic one 
