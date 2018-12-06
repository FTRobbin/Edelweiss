import getopt
import sys
import re

from Experiment.SynchronousByzantineSetting import *
from Experiment.Experiment import *
from Protocols.NaiveVoting import *
from Protocols.BOSCO import *
from Protocols.DolevStrong import *
from Protocols.Herding import *
from Measures.ByzantineMeasures import *
from Adversaries.CrashAdversary import *
from Controllers.SynController import *
from Controllers.SynController import *
from Adversaries.HalfHalfSenderAdversary import *
from Adversaries.SynBOSCOAgreementAttacker import *
from Adversaries.SynBOSCOAgreementCentralizedAttacker import *
from Test.Report import *
from test import *


SettingList = []


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            res = re.split(r'[\s\,]+', a)
            if not bool(res):
                raise RuntimeError
            settings = {}
            if res[0].isdigit():
                for i in range(len(res)):
                    run_and_print(demoProtocols[int(res[0])-1])
                sys.exit()
            elif res[0].isalpha():
                pass
            else:
                raise RuntimeError
        else:
            assert False, "unhandled option"
    # run_only(demoProtocols[-1])
    print(run_and_get_result(demoProtocols[-1]))


def usage():
    print("Usage: [options]")
    print("-h               Display help information")
    print("-i input list    Cases to be execuated")


if __name__ == "__main__":
    sys.setrecursionlimit(15000)
    for i in range(1000):
        main()
