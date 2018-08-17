from Test.ExpResult import *
from Util.Util import *
from Measures.ByzantineMeasures import *


class Experiment:

    id = 0

    def __init__(self, setting):
        self.id = Experiment.id
        Experiment.id += 1
        self.setting = setting
        self.controller = setting.con_type(setting)

    def run(self):
        self.controller.run()

    def report(self):
        print("Experiment Setting:")
        self.setting.report()
        print("")
        print("Experiment Result:")
        self.controller.report_message()
        print("")
        flag = 0
        if len(self.setting.measure) > 0:
            print("Measurements:")
            for m in self.setting.measure:
                flag = not (m.measure(self.controller))[1] or flag
                print(m.measure(self.controller)[
                      0], m.measure(self.controller)[1])
            if flag == 0:
                print(
                    "\033[1;32mCongrats! All properties are satisified! \033[0m")
            else:
                print("\033[1;31mOops! Some properties are violated! \033[0m")

    def run_and_report(self):
        self.run()
        self.report()

    def save_output(self):
        result = ExpResult(self.setting, self.controller)
        return (result.object_key(), result)

    def get_result(self):
        measure_dict = {}
        for m in self.setting.measure:
            measure_dict[m.measure(self.controller)[0]] = m.measure(
                self.controller)[1]
        return measure_dict


def AtomicStat(f, setting, times):
    stat_dict = {'Consistency': 0, 'Validity': 0, 'Unanimity': 0}
    for i in range(times):
        setting.set_seed(i)
        res = run_and_get_result(setting)
        for k, v in stat_dict.items():
            if res[k] == False:
                stat_dict[k] = v+1
    for k, v in stat_dict.items():
        stat_dict[k] = v/times
    print(stat_dict, file=f)
    if f:
        f.flush()


# set parameter and run


def SetStatParaAndRun(_file, setting, input, times, f, tf, protocol, adversary, _lambda=1, k=1, centralized=True):
    setting.set_input(input)
    setting.set_n(len(input))
    setting.set_f(f)
    setting.set_tf(tf)
    setting.set_protocol(protocol)
    setting.set_centralized(centralized)
    if centralized:
        setting.set_centralized_adversary(adversary)
    else:
        setting.set_adversary(adversary)
    setting.set_lambda(_lambda)
    setting.set_k(k)

    print("protocol="+setting.get_protocol().name, file=_file)
    if centralized:
        print("Centralized adversary!", file=_file)
        print("centralized_adversary=" +
              setting.get_centralized_adversary().name, file=_file)
    else:
        print("adversary="+setting.get_adversary().name, file=_file)
    print("times="+str(times), file=_file)
    print("k="+str(k), file=_file)
    print("lambda="+str(_lambda), file=_file)
    print("f="+str(f), file=_file)
    print("tf="+str(tf), file=_file)
    AtomicStat(_file, setting, times)  # atomtic one


def RunExperiment(h, input, times, _lambda_list, k_list, protocol_list, adversary_list, f_list):
    # Basic Herding with SynHerdingCentralizedValidity Attacker
    from Experiment.ExperimentSetting import SynchronousByzantine
    from Test.TestConfig import PossibleControllers
    setting = SynchronousByzantine(None, None, None,
                                   PossibleControllers[0], f=None, tf=None, protocol=None,
                                   measure=[ByzValidity,
                                            ByzConsistency, ByzUnanimity],
                                   centralized=None, centralized_adversary=None, seed=None, _lambda=None, k=None)
    for protocol in protocol_list:
        for adversary in adversary_list:
            for _lambda in _lambda_list:
                for k in k_list:
                    for f in f_list:
                        tf = f
                        SetStatParaAndRun(
                            h, setting, input, times, f, tf, protocol, adversary, _lambda, k)
                        print(" ", file=h)


def run_and_print(setting):
    exp = Experiment(setting)
    exp.run()
    res = exp.save_output()
    res[1].print()


def run_and_get_result(setting):
    exp = Experiment(setting)
    exp.run()
    return exp.get_result()
