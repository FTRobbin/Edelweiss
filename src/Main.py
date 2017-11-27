from Experiment import *
from ExperimentSetting import *
from Environment import *
from PKI import *
from NaiveVoting import *

setting = ExperimentSetting(10, 1, Environment, IdealPKI, NaiveVoting)
exp = Experiment(setting)
exp.run()
exp.report()
