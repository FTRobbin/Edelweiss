# fig main

from src.Experiment.PaxosSetting import *
from src.Experiment.Experiment import Experiment
from src.Measures.ByzantineMeasures import *

stat = []
rep = 1000
for n in [10, 15, 20, 25, 30]:
    for adv in [None, PaxosDDOS]:
        if adv is None:
            adv_name = 'None'
        else:
            adv_name = adv.name
        for protocol in [Paxos, FigPaxos]:
            succ = 0
            totalmsg = 0
            for seed in range(1, rep + 1):
                setting = PaxosSetting(n, protocol=protocol, seed=seed, adv=adv, measure=[MsgCount])
                exp = Experiment(setting)
                exp.run()
                m = exp.get_result()['cnt']
                if m != -1:
                    succ += 1
                    totalmsg += m
            if succ == 0:
                rate = 0
            else:
                rate = float(totalmsg) / succ
            print('n=%d adv=%s protocol=%s | Succ %d/%d, SuccRate %.2f, AvgMsg %.2f AvAvMsg %.2f' % (n, adv_name, protocol.name, succ, rep, float(succ)/rep * 100, rate, rate/n))
            stat.append(rate)
print(stat)
