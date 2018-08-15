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
from Adversaries.SynBOSCOAgreementAttacker import *
from Adversaries.SynBOSCOAgreementCentralizedAttacker import *
from Adversaries.SynHerdingAgreementAttacker import *
from Adversaries.SynHerdingCentralizedAgreementAttacker import *
from Adversaries.SynHerdingBenchmarkAttacker import *
from Test.TestConfig import *


def generate_benchmark():
    
    jsonfile = {}
    for ProtocolList in TestProtocolsList:
        
        for setting in ProtocolList:
            exp = Experiment(setting)
            exp.run()
            res = exp.save_output()
            jsonfile[res[0]] = res[1]
    serialized = jsonpickle.encode(jsonfile)
    with open("../data/benchmark.json", 'w+') as f:
        print(serialized, file=f)
    print("Benchmark has been successfully generated!!!")


def test(ProtocolsList):
    with open('../data/benchmark.json', 'r') as f:
        content = f.read()
        data = jsonpickle.decode(content)
    cnt = 0
    for ProtocolList in ProtocolsList:
        ProtocolName = [ k for k,v in globals().items() if v is ProtocolList][0]
        print("testing "+ProtocolName)
        flag=0
        for setting in ProtocolList:
            exp = Experiment(setting)
            exp.run()
            res = exp.save_output()
            if res[0] not in data.keys():
                raise RuntimeError
            current_data = data[res[0]]
            if not operator.eq(current_data.round_history, res[1].round_history):
                flag=1
                print("%s test failed on round_history" % str(setting))
                continue
            if not operator.eq(current_data.output, res[1].output):
                flag=1
                print("%s test failed on output" % str(setting))
                continue
        if flag==0:
            print('Test %s passed!' % ProtocolName)
            cnt += 1
        else:
            print('Test %s failed!' % ProtocolName)
    if(cnt == len(ProtocolsList)):
        print('All tests passed! (%(numerator)d/%(denumerator)d)' %
              {'numerator': cnt, "denumerator": cnt})
    else:
        print('Some test(s) failed! (%(numerator)d/%(denumerator)d)' %
              {'numerator': cnt, "denumerator": len(ProtocolsList)})


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:g", ["help", "input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
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
                    TestProtocolsList.index(x)+1) in res, TestProtocolsList))
            elif res[0].isalpha():
                pass
            else:
                raise RuntimeError
            test(settings)
            sys.exit()
        else:
            assert False, "unhandled option"
    test(TestProtocolsList)


def usage():
    print("Usage: [options]")
    print("-h               Display help information")
    print("-i input list    test cases to be execuated")
    print("-g               generate benchmark")


if __name__ == "__main__":
    main()
