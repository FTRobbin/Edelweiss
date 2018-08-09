import random

from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Test.Report import *
from test import *
from Stat.AdversaryStat import *
from Stat.Stat import *

def SynHerdingValidityAttackStat():
    input=5*[1]+5*[0]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    k=8
    _lambda_loacl=1
    setting = SynchronousByzantine(10, input, PossibleAdversaries[4],
                                   PossibleControllers[0], f=5, tf=5, protocol=Herding,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[5], seed=None, _lambda=_lambda_loacl,k=1)
    f_list=[5]
    setting.set_k(k)
    print("k="+str(k))
    print("lambda="+str(_lambda_loacl))
    for f in f_list:
        print("f="+str(f))
        tf=f
        stat(setting,input,f,tf,_lambda_loacl,1)
