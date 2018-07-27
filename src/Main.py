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

PossibleControllers = [SynByzController, SynByzController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentralizedAttacker]
setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                               PossibleControllers[1], f=0, tf=0, protocol=NaiveVoting,
                               measure=[ByzValidity, ByzConsistency, ByzUnanimity],
                               centralized=True, centralized_adversary=PossibleAdversaries[3],
                               has_sender=True, corrupt_sender=False)
exp = Experiment(setting)
exp.run()
exp.report()

# setting = AsynchronousByzantine(n=1, input=1, protocol=BenOr, measure=[ByzValidity, ByzConsistency])
# exp = Experiment(setting)
# exp.run()
# exp.report()

# setting = SynchronousByzantine(10, [1, 1, 1, 1, 0, 0, 0, 1, 1, 1], PossibleAdversaries[2],
#                                             PossibleControllers[1], f=3, tf=3, protocol=BOSCO,
#                                             measure=[ByzValidityWithoutSender, ByzConsistency, ByzUnanimity],
#                                             centralized=True, centralized_adversary=PossibleAdversaries[3])
# exp = Experiment(setting)
# exp.run()
# exp.report()
# exp.run_and_report()
# setting2 = SynchronousByzantine(10, 1, PossibleAdversaries[2],
#                                             PossibleControllers[1], f=0, tf=0,protocol=DolevStrong,
#                                             measure=[ByzValidity, ByzConsistency,ByzUnanimity],
#                                             centralized=False, centralized_adversary=PossibleAdversaries[3], 
#                                             has_sender=True,corrupt_sender=False)
# exp2 = Experiment(setting2)
# exp2.run_and_report()
