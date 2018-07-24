from Experiment.ExperimentSetting import *
from Experiment.Experiment import *
from Protocols.NaiveVoting import *
from Protocols.BOSCO import *
from Protocols.DolevStrong import *
from Measures.ByzantineMeasures import *

# setting = SynchronousByzantine(n=10, input=1, protocol=NaiveVoting, measure=[ByzValidity, ByzConsistency])
# exp = Experiment(setting)
# exp.run()
# exp.report()

# setting = AsynchronousByzantine(n=1, input=1, protocol=BenOr, measure=[ByzValidity, ByzConsistency])
# exp = Experiment(setting)
# exp.run()
# exp.report()
setting = SynchronousByzantineWithoutSender(n=6,f=1,input=[1]*6, protocol=BOSCO, measure=[ByzValidityWithoutSender, ByzConsistency,ByzUnanimity])
exp = Experiment(setting)
exp.run()
exp.report()
# exp.run_and_report()
# setting2 = SynchronousByzantine(n=10, input=1, protocol=DolevStrong, measure=[ByzValidity, ByzConsistency])
# exp2 = Experiment(setting2)
# exp2.run_and_report()
