from Test.TestConfig import *
from Protocols.HerdingWithBroadcastFast import *
from Experiment.Experiment import *
from Util.Util import get_host_ip
seed_map = {
    43: 0,
    71: 100,
    76: 300,
    79: 500,
    84: 700,
    87: 900,
    88: 1100,
    121: 1300,
    140: 1500,
    154: 1700,
    157: 1900}


def IOTAStat(times=1):
    h = open("IOTAStat30.txt", "w+")
    protocol_list = [IOTA]
    adversary_list = [PossibleAdversaries[8]]
    f_list = [30]
    node_num = 100
    ip = get_host_ip()
    ip_id = int(ip.split('.')[-1])
    seed = seed_map[ip_id]
    RunIOTAExperiment(h, node_num, times, protocol_list,
                      adversary_list, f_list, seed)
    h.close()
