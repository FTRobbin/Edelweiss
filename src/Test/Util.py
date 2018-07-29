import operator

import jsonpickle

from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Protocols.NaiveVoting import *
from Protocols.BOSCO import *
from Protocols.DolevStrong import *
from Measures.ByzantineMeasures import *
from Adversaries.CrashAdversary import *
from Controllers.SynByzController import *
from Controllers.SynByzController import *
from Adversaries.HalfHalfSenderAdversary import *
from Adversaries.SynBOSCOValidityAttacker import *
from Adversaries.SynBOSCOValidityCentralizedAttacker import *

PossibleControllers = [SynByzController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentralizedAttacker]


def generate_benchmark():
    jsonfile = {}
    # 1 NaiveVoting
    setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                   PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3],
                                   has_sender=True, corrupt_sender=False)
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    jsonfile[res[0]] = res[1]
    # 2 DecentralizedBoscoRight
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                   PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    jsonfile[res[0]] = res[1]

    # 3 DicentralizedBoscoWrong
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                   PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    jsonfile[res[0]] = res[1]

    # 4 CentralizedBoscoRight
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                   PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=True, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    jsonfile[res[0]] = res[1]

    # 5 CentralizedBoscoWrong
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                   PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=True, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    jsonfile[res[0]] = res[1]

    # 6 DolevStrong
    setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                   PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3],
                                   has_sender=True, corrupt_sender=False)
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    jsonfile[res[0]] = res[1]
    serialized = jsonpickle.encode(jsonfile)
    with open("../data/benchmark.json", 'w+') as f:
        print(serialized, file=f)


def test():
    with open('../data/benchmark.json', 'r') as f:
        content = f.read()
        data = jsonpickle.decode(content)
    # 1 NaiveVoting
    setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                   PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3],
                                   has_sender=True, corrupt_sender=False)
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    if res[0] not in data.keys():
        raise RuntimeError
    current_data = data[res[0]]
    assert operator.eq(current_data.round_history, res[1].round_history)
    assert operator.eq(current_data.output, res[1].output)

    # 2 DecentralizedBoscoRight
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                   PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    if res[0] not in data.keys():
        raise RuntimeError
    current_data = data[res[0]]
    assert operator.eq(current_data.round_history, res[1].round_history)
    assert operator.eq(current_data.output, res[1].output)

    # 3 DecentralizedBoscoWrong
    setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                   PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3],
                                   has_sender=True, corrupt_sender=False)
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    if res[0] not in data.keys():
        raise RuntimeError
    current_data = data[res[0]]
    assert operator.eq(current_data.round_history, res[1].round_history)
    assert operator.eq(current_data.output, res[1].output)

    # 4 CentralizedBoscoRight
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                   PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=True, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    if res[0] not in data.keys():
        raise RuntimeError
    current_data = data[res[0]]
    assert operator.eq(current_data.round_history, res[1].round_history)
    assert operator.eq(current_data.output, res[1].output)

    # 5 CentralizedBoscoWrong
    setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                   PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=True, centralized_adversary=PossibleAdversaries[3])
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    if res[0] not in data.keys():
        raise RuntimeError
    current_data = data[res[0]]
    assert operator.eq(current_data.round_history, res[1].round_history)
    assert operator.eq(current_data.output, res[1].output)

    # 6 DolevStrong
    setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                   PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=False, centralized_adversary=PossibleAdversaries[3],
                                   has_sender=True, corrupt_sender=False)
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    if res[0] not in data.keys():
        raise RuntimeError
    current_data = data[res[0]]
    assert operator.eq(current_data.round_history, res[1].round_history)
    assert operator.eq(current_data.output, res[1].output)
