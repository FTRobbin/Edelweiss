import operator
import getopt
import sys
import re

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
SettingNumToNameDict = {'1': "NaiveVoting", '2': "DecentralizedBosco", '3': "DicentralizedBoscValidityAttack", '4': "CentralizedBosco",
                        '5': "CentralizedBoscoValidityAttack", '6': "DolevStrong"}
SettingDict = {"NaiveVoting": SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                                   PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                   measure=[ByzValidity,
                                                            ByzConsistency, ByzUnanimity],
                                                   centralized=False, centralized_adversary=PossibleAdversaries[
                                                       3],
                                                   has_sender=True, corrupt_sender=False),
               "DecentralizedBosco": SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                          PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                                          measure=[ByzValidity,
                                                                   ByzConsistency, ByzUnanimity],
                                                          centralized=False, centralized_adversary=PossibleAdversaries[3]),
               "DicentralizedBoscValidityAttack": SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                                       PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                                       measure=[ByzValidity,
                                                                                ByzConsistency, ByzUnanimity],
                                                                       centralized=False, centralized_adversary=PossibleAdversaries[3]),
               "CentralizedBosco": SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                                        PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                                        measure=[ByzValidity,
                                                                 ByzConsistency, ByzUnanimity],
                                                        centralized=True, centralized_adversary=PossibleAdversaries[3]),
               "CentralizedBoscoValidityAttack": SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                                                      PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                                      measure=[ByzValidity,
                                                                               ByzConsistency, ByzUnanimity],
                                                                      centralized=True, centralized_adversary=PossibleAdversaries[3]),
               "DolevStrong": SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                                   PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                                   measure=[ByzValidity,
                                                            ByzConsistency, ByzUnanimity],
                                                   centralized=False, centralized_adversary=PossibleAdversaries[
                                                       3],
                                                   has_sender=True, corrupt_sender=False)}


def generate_benchmark():
    jsonfile = {}
    for name, setting in SettingDict.items():
        exp = Experiment(setting)
        exp.run()
        res = exp.save_output()
        jsonfile[res[0]] = res[1]
    serialized = jsonpickle.encode(jsonfile)
    with open("../data/benchmark.json", 'w+') as f:
        print(serialized, file=f)
    print("Benchmark has been successfully generated!!!")


def test(settings):
    with open('../data/benchmark.json', 'r') as f:
        content = f.read()
        data = jsonpickle.decode(content)
    cnt = 0
    for name, setting in settings.items():
        exp = Experiment(setting)
        exp.run()
        res = exp.save_output()
        if res[0] not in data.keys():
            raise RuntimeError
        current_data = data[res[0]]
        if not operator.eq(current_data.round_history, res[1].round_history):
            print("%s test failed" % name)
            continue
        if not operator.eq(current_data.output, res[1].output):
            print("%s test failed" % name)
            continue
        cnt += 1
        print('Tests %s passed!' % name)
    if(cnt == len(settings)):
        print('All tests passed! (%(numerator)d/%(denumerator)d)' %
              {'numerator': cnt, "denumerator": cnt})
    else:
        print('Some tests failer! (%(numerator)d/%(denumerator)d)' %
              {'numerator': len(settings)-cnt, "denumerator": len(settings)})


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:g", ["help", "input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-g":
            generate_benchmark()
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            res = re.split(r'[\s\,]+', a)
            if not bool(res):
                raise RuntimeError
            settings = {}
            if res[0].isdigit():
                for k, v in SettingNumToNameDict.items():
                    if k in res:
                        settings[SettingNumToNameDict[k]
                                 ] = SettingDict[SettingNumToNameDict[k]]
            elif res[0].isalpha():
                for k, v in SettingDict.items():
                    if k in res:
                        settings[k] = v
            else:
                raise RuntimeError
            test(settings)
            sys.exit()
        else:
            assert False, "unhandled option"
    test(SettingDict)


def usage():
    print("Usage: [options]")
    print("-h               Display help information")
    print("-i input list    test cases to be execuated")
    print("-g               generate benchmark")


if __name__ == "__main__":
    main()
