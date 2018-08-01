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
from Test.Report import *

PossibleControllers = [SynByzController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentralizedAttacker]
# setting = SynchronousByzantine(10, 1, PossibleAdversaries[2],
#                                PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
#                                measure=[ByzValidity,
#                                         ByzConsistency, ByzUnanimity],
#                                centralized=True, centralized_adversary=PossibleAdversaries[3],
#                                has_sender=True, corrupt_sender=False)
# exp = Experiment(setting)
# exp.run_and_report()
# jsonfile = {}
# res = exp.save_output()
# jsonfile[res[0]]=res[1]
# serialized = jsonpickle.encode(res)
# setting = AsynchronousByzantine(n=1, input=1, protocol=BenOr, measure=[ByzValidity, ByzConsistency])
# exp = Experiment(setting)
# exp.run()
# exp.report()

# setting = SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
#                                             PossibleControllers[0], f=3, protocol=BOSCO, tf=4,
#                                             measure=[ByzValidity, ByzConsistency, ByzUnanimity],
#                                             centralized=True, centralized_adversary=PossibleAdversaries[3])
# exp = Experiment(setting)
# exp.run_and_report()
# res= exp.save_output()
# jsonfile[res[0]] = res[1]
# serialized = jsonpickle.encode(jsonfile)
# print (serialized)
# generate_benchmark()
# Report()
# exp.report()
# exp.run_and_report()
setting2 = SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                            PossibleControllers[0], f=0, tf=0,protocol=DolevStrong,
                                            measure=[ByzValidity, ByzConsistency,ByzUnanimity],
                                            centralized=False, centralized_adversary=PossibleAdversaries[3],
                                            has_sender=True,corrupt_sender=False)
exp2 = Experiment(setting2)
exp2.run_and_report()
# setting = SynchronousByzantine(5, [1, 0,0,1,1], PossibleAdversaries[3],
#                                PossibleControllers[0], f=0, tf=0, protocol=Herding,
#                                measure=[ByzValidity,
#                                         ByzConsistency, ByzUnanimity],
#                                centralized=False, centralized_adversary=PossibleAdversaries[3],seed=None,_lambda=3)
# exp = Experiment(setting)
# exp.run_and_report()
