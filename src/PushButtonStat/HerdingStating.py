from Stat.AdversaryStat import *
from test import *

def HerdingStating():
    # Basic Herding with SynHerdingCentralizedValidity Attacker
    print("I am running")
    input=50*[1]+50*[1]
    times=1000
    _lambda_list=[1]
    k_list=[1,4,8,16,32]
    protocol_list=[Herding]
    adversary_list=[PossibleAdversaries[5],PossibleAdversaries[6]]
    f_list=[0]
    for protocol in protocol_list:
        for adversary in adversary_list:
            for _lambda in _lambda_list:
                for k in k_list: 
                    SynHerdingValidityAttackStat(input,times,k,_lambda,f_list,protocol,adversary)
                    print(" ")



