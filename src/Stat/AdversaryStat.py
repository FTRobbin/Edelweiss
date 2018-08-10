import random

from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Test.Report import *
from test import *
from Stat.AdversaryStat import *
from Stat.Stat import *
from Protocols.HerdingWithBroadcast import *
from Adversaries.SynHerdingBenchmarkAttacker import *
def SynHerdingValidityAttackStat():
    input=5*[1]+5*[0]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    k=4
    _lambda_loacl=1
    setting = SynchronousByzantine(10, input, PossibleAdversaries[4],
                                   PossibleControllers[0], f=0, tf=0, protocol=Herding,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=True, centralized_adversary=PossibleAdversaries[5], seed=None, _lambda=_lambda_loacl,k=1)
    f_list=[3,4,5,6]
    setting.set_k(k)
    print("k="+str(k))
    print("lambda="+str(_lambda_loacl))
    for f in f_list:
        print("f="+str(f))
        tf=f
        stat(setting,input,f,tf,_lambda_loacl,1000)
