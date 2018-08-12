from Protocols.Herding import *
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
from Adversaries.SynHerdingValidityAttacker import *
from Adversaries.SynHerdingCentralizedValidityAttacker import *
from Adversaries.SynHerdingBenchmarkAttacker import *

PossibleControllers = [SynByzController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentralizedAttacker, SynHerdingValidityAttacker, SynHerdingCentralizedValidityAttacker, SynHerdingBenchmarkAttacker]

#################### Navie Voting Begin #########################
#################### Navie Voting Begin #########################
#################### Navie Voting Begin #########################
NaiveVotingTestList = [SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                            PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                            measure=[ByzValidity,
                                                     ByzConsistency, ByzUnanimity],
                                            centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),  # Navie Voting 1
    SynchronousByzantine(10, 0, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),  # Navie Voting 2

    SynchronousByzantine(5, 1, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),  # Navie Voting 3



    SynchronousByzantine(5, 0, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),  # Navie Voting 4

    SynchronousByzantine(20, 1, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False)]  # Navie Voting 5
#################### Navie Voting End #########################
#################### Navie Voting End #########################
#################### Navie Voting End #########################

#################### Decentralized Bosco Start #########################
#################### Decentralized Bosco Start #########################
#################### Decentralized Bosco Start #########################

DecentralizedBoscoTestList = [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                   PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                                   measure=[ByzValidity,
                                                            ByzConsistency, ByzUnanimity],
                                                   centralized=False, centralized_adversary=PossibleAdversaries[3])]

#################### Decentralized Bosco End #########################
#################### Decentralized Bosco End #########################
#################### Decentralized Bosco End #########################

#################### Decentralized Bosco Attack Start #########################
#################### Decentralized Bosco Attack Start #########################
#################### Decentralized Bosco Attack Start #########################

DecentralizedBoscoValidityAttackTestList = [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                                 PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                                 measure=[ByzValidity,
                                                                          ByzConsistency, ByzUnanimity],
                                                                 centralized=False, centralized_adversary=PossibleAdversaries[3])
                                            ]

#################### Decentralized Bosco Attack End #########################
#################### Decentralized Bosco Attack End #########################
#################### Decentralized Bosco Attack End #########################

#################### Centralized Bosco Start #########################
#################### Centralized Bosco Start #########################
#################### Centralized Bosco Start #########################


CentralizedBoscoTestList = [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                                 PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                                 measure=[ByzValidity,
                                                          ByzConsistency, ByzUnanimity],
                                                 centralized=True, centralized_adversary=PossibleAdversaries[3])]

#################### Centralized Bosco End #########################
#################### Centralized Bosco End #########################
#################### Centralized Bosco End #########################

#################### Centralized Bosco Attack Start #########################
#################### Centralized Bosco Attack Start #########################
#################### Centralized Bosco Attack Start #########################

CentralizedBoscoValidityAttackTestList = [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1,
                                                                    ], PossibleAdversaries[3],
                                                               PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                               measure=[ByzValidity,
                                                                        ByzConsistency, ByzUnanimity],
                                                               centralized=True, centralized_adversary=PossibleAdversaries[3])]
#################### Centralized Bosco Attack End #########################
#################### Centralized Bosco Attack End #########################
#################### Centralized Bosco Attack End #########################

#################### DolevString Start  #########################
#################### DolevString Start  #########################
#################### DolevString Start  #########################

DolevStrongTestList = [SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                            PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                            measure=[ByzValidity,
                                                     ByzConsistency, ByzUnanimity],
                                            centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(10, 0, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(20, 1, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(20, 0, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(20, 1, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False)]
#################### DolevString End  #########################
#################### DolevString End  #########################
#################### DolevString End  #########################

#################### Herding Start  #########################
#################### Herding Start  #########################
#################### Herding Start  #########################
HerdingTestListTestList = [SynchronousByzantine(10, [0, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                                                     ], PossibleAdversaries[3],
                                                PossibleControllers[0], f=0, tf=0, protocol=Herding,
                                                measure=[ByzValidity,
                                                         ByzConsistency, ByzUnanimity],
                                                centralized=False, centralized_adversary=PossibleAdversaries[3], seed=0, _lambda=3)]
#################### Herding End  #########################
#################### Herding End  #########################
#################### Herding End  #########################

#################### Herding Validity Attack Start  #########################
#################### Herding Validity Attack Start  #########################
#################### Herding Validity Attack Start  #########################
HerdingValidityAttackTestList = [SynchronousByzantine(10, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], PossibleAdversaries[4],
                                                      PossibleControllers[0], f=5, tf=5, protocol=Herding,
                                                      measure=[ByzValidity,
                                                               ByzConsistency, ByzUnanimity],
                                                      centralized=False, centralized_adversary=PossibleAdversaries[3], seed=4, _lambda=4, k=4)
                                 ]
#################### Herding Validity Attack End  #########################
#################### Herding Validity Attack End  #########################
#################### Herding Validity Attack End  #########################
TestProtocolsList = [NaiveVotingTestList, DecentralizedBoscoTestList, DecentralizedBoscoValidityAttackTestList, DecentralizedBoscoValidityAttackTestList,
                     CentralizedBoscoTestList, CentralizedBoscoValidityAttackTestList, DolevStrongTestList, HerdingTestListTestList, HerdingValidityAttackTestList]
demoProtocols = [SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                                     PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                     measure=[ByzValidity,
                                                              ByzConsistency, ByzUnanimity],
                                                     centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),
     SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                               PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                               measure=[ByzValidity,
                                                        ByzConsistency, ByzUnanimity],
                                               centralized=False, centralized_adversary=PossibleAdversaries[3]),
    SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                            PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                            measure=[ByzValidity,
                                                                     ByzConsistency, ByzUnanimity],
                                                            centralized=False, centralized_adversary=PossibleAdversaries[3]),
    SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                             PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                             measure=[ByzValidity,
                                                      ByzConsistency, ByzUnanimity],
                                             centralized=True, centralized_adversary=PossibleAdversaries[3]),
    SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                                           PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                           measure=[ByzValidity,
                                                                    ByzConsistency, ByzUnanimity],
                                                           centralized=True, centralized_adversary=PossibleAdversaries[3]),
     SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                        PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(10, [0, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                                                     ], PossibleAdversaries[3],
                                                PossibleControllers[0], f=0, tf=0, protocol=Herding,
                                                measure=[ByzValidity,
                                                         ByzConsistency, ByzUnanimity],
                                                centralized=False, centralized_adversary=PossibleAdversaries[3], seed=0,k=4, _lambda=3),
    SynchronousByzantine(10, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], PossibleAdversaries[4],
                                                      PossibleControllers[0], f=5, tf=5, protocol=Herding,
                                                      measure=[ByzValidity,
                                                               ByzConsistency, ByzUnanimity],
                                                      centralized=False, centralized_adversary=PossibleAdversaries[3], seed=4, _lambda=4, k=4)
                                 ]
