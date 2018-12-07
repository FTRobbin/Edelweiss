from Test.TestConfig import *
from Protocols.HerdingWithBroadcastFast import *
from Experiment.Experiment import *
from Util.Util import get_host_ip
seed_map = {
    56: 0,
    248: 100,
    213: 300,
    195: 500,
    207: 700,
    194: 900,
    184: 1100,
    160: 1300,
    225: 1500,
    211: 1700,
    224: 1900}


def IOTAStat(times=1):
    h = open("IOTAStatStat.txt", "w+")
    protocol_list = [IOTA]
    adversary_list = [PossibleAdversaries[8]]
    f_list = [3]
    node_num = 25
    ip = get_host_ip()
    ip_id = int(ip.split('.')[-1])
    seed = seed_map[ip_id]
    _lambda_list=[1]
    RunIOTAExperiment(h, node_num, times, protocol_list,
                      adversary_list, f_list, seed,_lambda_list)
    f_list = [4]
    node_num = 50
    RunIOTAExperiment(h, node_num, times, protocol_list,
                    adversary_list, f_list, seed,_lambda_list)
    f_list = [5]
    node_num = 100
    RunIOTAExperiment(h, node_num, times, protocol_list,
                    adversary_list, f_list, seed,_lambda_list)
    h.close()

