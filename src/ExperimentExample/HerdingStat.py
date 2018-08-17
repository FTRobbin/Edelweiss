from Test.TestConfig import *
from Protocols.HerdingWithBroadcastFast import *
from Experiment.Experiment import *



def HerdingStat(times=1):
    h = open("HerdingStat.txt", "w+")
    input = 50*[1]+50*[0]
    # Experiment 1: Broken without broadcast
    protocol_list = [Herding]
    adversary_list = [PossibleAdversaries[4]]
    _lambda_list = [2]
    k_list = [5, 10, 15, 20, 25, 30]
    f_list = [20]
    RunExperiment(h, input, times, _lambda_list, k_list, protocol_list, adversary_list, f_list)
    # Experiment 2: Round, F, Bruteforce
    # Experiment 3: Round, F, Advanced
    protocol_list = [HerdingWithBroadcastFast]
    adversary_list = [PossibleAdversaries[4], PossibleAdversaries[5]]
    _lambda_list = [2]
    f_list = [20, 25, 30, 35, 40, 45, 50, 55, 60]
    RunExperiment(h, input, times, _lambda_list, k_list, protocol_list, adversary_list, f_list)
    h.close()

