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
from Protocols.Herding import *
from Measures.ByzantineMeasures import *
from Adversaries.CrashAdversary import *
from Controllers.SynByzController import *
from Controllers.SynByzController import *
from Adversaries.HalfHalfSenderAdversary import *
from Adversaries.SynBOSCOValidityAttacker import *
from Adversaries.SynBOSCOValidityCentralizedAttacker import *
from Adversaries.SynHerdingValidityAttacker import *
from Adversaries.SynHerdingCentralizedValidityAttacker import *

PossibleControllers = [SynByzController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentralizedAttacker, SynHerdingValidityAttacker,SynHerdingCentralizedValidityAttacker]




def generate_benchmark():
    jsonfile = {}
    for (name, setting) in SettingList:
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
    for (name, setting) in settings:
        exp = Experiment(setting)
        exp.run()
        res = exp.save_output()
        if res[0] not in data.keys():
            raise RuntimeError
        current_data = data[res[0]]
        if not operator.eq(current_data.round_history, res[1].round_history):
            print("%s test failed on round_history" % name)
            continue
        if not operator.eq(current_data.output, res[1].output):
            print("%s test failed on output" % name)
            continue
        cnt += 1
        print('Test %s passed!' % name)
    if(cnt == len(settings)):
        print('All tests passed! (%(numerator)d/%(denumerator)d)' %
              {'numerator': cnt, "denumerator": cnt})
    else:
        print('Some test(s) failed! (%(numerator)d/%(denumerator)d)' %
              {'numerator': cnt, "denumerator": len(settings)})


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
                settings = list(filter(lambda x: str(
                    SettingList.index(x)+1) in res, SettingList))
            elif res[0].isalpha():
                pass
            else:
                raise RuntimeError
            test(settings)
            sys.exit()
        else:
            assert False, "unhandled option"
    test(SettingList)


def usage():
    print("Usage: [options]")
    print("-h               Display help information")
    print("-i input list    test cases to be execuated")
    print("-g               generate benchmark")


if __name__ == "__main__":
    main()
