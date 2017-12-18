from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Protocols.NaiveVoting import *
from Measures.ByzantineMeasures import *

setting = SynchronousByzantine(n=10, input=1, protocol=NaiveVoting, measure=[ByzValidity, ByzConsistency])
exp = Experiment(setting)
exp.run()
exp.report()
