from Stat.AdversaryStat import *
from test import *

def HerdingStat():
    # Basic Herding with SynHerdingCentralizedValidity Attacker
    input=50*[1]+50*[0]
    times=1000
    _lambda_list=[4]
    k_list=[4,8,16]
    protocol_list=[Herding,HerdingWithBroadcast]
    adversary_list=[PossibleAdversaries[5],PossibleAdversaries[6]]
    f_list=[27,33,38,44,50,55]
    for protocol in protocol_list:
        for adversary in adversary_list:
            for _lambda in _lambda_list:
                for k in k_list: 
                    SynHerdingValidityAttackStat(input,times,k,_lambda,f_list,protocol,adversary)
                    print(" ")



