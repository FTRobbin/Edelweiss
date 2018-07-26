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
OptionalControllers = [SynByzController, SynByzControllerWithoutSender, SynByzControllerCentroliezedAdversary]
OptionalAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentrolizedAttacker]
setting = SynchronousByzantineWithoutSender(10, [1, 1, 1, 1, 0, 0, 0, 1, 1, 1], OptionalAdversaries[1],
                                            OptionalControllers[1], f=3, tf=4, protocol=BOSCO,
                                            measure=[ByzValidityWithoutSender, ByzConsistency, ByzUnanimity])
exp = Experiment(setting)
exp.run()
exp.report()
# exp.run_and_report()
# setting2 = SynchronousByzantine(n=10, input=1, protocol=DolevStrong, measure=[ByzValidity, ByzConsistency])
# exp2 = Experiment(setting2)
# exp2.run_and_report()
