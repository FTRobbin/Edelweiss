from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Protocols.NaiveVoting import *
from Protocols.BOSCO import *
from Measures.ByzantineMeasures import *

# setting = SynchronousByzantine(n=10, input=1, protocol=NaiveVoting, measure=[ByzValidity, ByzConsistency])
# exp = Experiment(setting)
# exp.run()
# exp.report()

# setting = AsynchronousByzantine(n=1, input=1, protocol=BenOr, measure=[ByzValidity, ByzConsistency])
# exp = Experiment(setting)
# exp.run()
# exp.report()

setting = SynchronousByzantineWithoutSender(n=10,f=0,input=[1]*10, protocol=BOSCO, measure=[ByzValidityWithoutSender, ByzConsistency,ByzUnanimity])
exp = Experiment(setting)
exp.run()
exp.report()