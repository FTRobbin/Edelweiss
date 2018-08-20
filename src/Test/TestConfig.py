from Experiment.SynchronousByzantineSetting import *
from Experiment.AsynSetting import *
from Experiment.Experiment import *
from Protocols.NaiveVoting import *
from Protocols.Herding import *
from Protocols.BOSCO import *
from Protocols.DolevStrong import *
from Protocols.Herding import *
from Protocols.HerdingWithBroadcastFast import *
from Protocols.DolevStrong_Wrong import *
from Protocols.Nakamoto import *
from Measures.ByzantineMeasures import *
from Adversaries.CrashAdversary import *
from Controllers.SynController import *
from Controllers.AsynPermissionedController import *
from Adversaries.HalfHalfSenderAdversary import *
from Adversaries.SynBOSCOAgreementAttacker import *
from Adversaries.SynBOSCOAgreementCentralizedAttacker import *
from Adversaries.SynHerdingBenchmarkAttacker import *
from Adversaries.SynHerdingAgreementFast import *
from Adversaries.DolevStrongRoundAdversary import *

PossibleControllers = [SynController,AsynPermissionedController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOAgreementAttacker, SynBOSCOAgreementCentralizedAttacker, SynHerdingBenchmarkAttacker, SynHerdingAgreementFast,DolevStrongRoundAdversary]

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

        SynchronousByzantine(5, 1, PossibleAdversaries[1],
                                        PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=False, corrupt_sender=False),  # Navie Voting 3



    SynchronousByzantine(5, 0, PossibleAdversaries[2],
                         PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                         measure=[ByzValidity,
                                  ByzConsistency, ByzUnanimity],
                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
    has_sender=True, corrupt_sender=False),  # Navie Voting 4

    SynchronousByzantine(5, 1, PossibleAdversaries[1],
                                        PossibleControllers[0], f=1, tf=1, protocol=NaiveVoting,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True)]  # Navie Voting 5
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

DecentralizedBoscoAgreementAttackTestList = [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
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

CentralizedBoscoAgreementAttackTestList = [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1,
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
    SynchronousByzantine(5, 1, PossibleAdversaries[0],
                                        PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(5, 1, PossibleAdversaries[0],
                                        PossibleControllers[0], f=2, tf=2, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(5, 1, PossibleAdversaries[0],
                                        PossibleControllers[0], f=1, tf=1, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True),
   SynchronousByzantine(5, 1, PossibleAdversaries[1],
                                        PossibleControllers[0], f=1, tf=1, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True),
    SynchronousByzantine(5, 1, PossibleAdversaries[6],
                                        PossibleControllers[0], f=3, tf=3, protocol=DolevStrong_Wrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True)]
#################### DolevString End  #########################
#################### DolevString End  #########################
#################### DolevString End  #########################

#################### Herding Start  #########################
#################### Herding Start  #########################
#################### Herding Start  #########################
HerdingTestListTestList = [SynchronousByzantine(10, [0, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                                                     ], PossibleAdversaries[3],
                                                PossibleControllers[0], f=0, tf=0, protocol=HerdingWithBroadcastFast,
                                                measure=[ByzValidity,
                                                         ByzConsistency, ByzUnanimity],
                                                centralized=False, centralized_adversary=PossibleAdversaries[3], seed=0, _lambda=3)]
#################### Herding End  #########################
#################### Herding End  #########################
#################### Herding End  #########################

#################### Herding Agreement Attack Start  #########################
#################### Herding Agreement Attack Start  #########################
#################### Herding Agreement Attack Start  #########################
HerdingAgreementAttackTestList = [SynchronousByzantine(10, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], PossibleAdversaries[4],
                                                      PossibleControllers[0], f=5, tf=5, protocol=HerdingWithBroadcastFast,
                                                      measure=[ByzValidity,
                                                               ByzConsistency, ByzUnanimity],
                                                      centralized=True, centralized_adversary=PossibleAdversaries[4], seed=4, _lambda=4, k=4)
                                 ,SynchronousByzantine(10, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], PossibleAdversaries[5],
                                                      PossibleControllers[0], f=5, tf=5, protocol=HerdingWithBroadcastFast,
                                                      measure=[ByzValidity,
                                                               ByzConsistency, ByzUnanimity],
                                                      centralized=True, centralized_adversary=PossibleAdversaries[5], seed=4, _lambda=4, k=4)
                                 ]
#################### Herding Agreement Attack End  #########################
#################### Herding Agreement Attack End  #########################
#################### Herding Agreement Attack End  #########################
TestProtocolsList = [NaiveVotingTestList, DecentralizedBoscoTestList, DecentralizedBoscoAgreementAttackTestList, DecentralizedBoscoAgreementAttackTestList,
                     CentralizedBoscoTestList, CentralizedBoscoAgreementAttackTestList, DolevStrongTestList, HerdingTestListTestList, HerdingAgreementAttackTestList]
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
                                                PossibleControllers[0], f=0, tf=0, protocol=HerdingWithBroadcastFast,
                                                measure=[ByzValidity,
                                                         ByzConsistency, ByzUnanimity],
                                                centralized=False, centralized_adversary=PossibleAdversaries[3], seed=0,k=4, _lambda=3),
    SynchronousByzantine(10, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], PossibleAdversaries[4],
                                                      PossibleControllers[0], f=5, tf=5, protocol=HerdingWithBroadcastFast,
                                                      measure=[ByzValidity,
                                                               ByzConsistency, ByzUnanimity],
                                                      centralized=True, centralized_adversary=PossibleAdversaries[5], seed=4, _lambda=4, k=4),
    SynchronousByzantine(5, 1, PossibleAdversaries[1],
                                        PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(5, 1, PossibleAdversaries[0],
                                        PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=False),
    SynchronousByzantine(5, 1, PossibleAdversaries[0],
                                        PossibleControllers[0], f=1, tf=1, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True),
    SynchronousByzantine(5, 1, PossibleAdversaries[1],
                                        PossibleControllers[0], f=1, tf=1, protocol=DolevStrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True),
    SynchronousByzantine(5, 1, PossibleAdversaries[1],
                                        PossibleControllers[0], f=1, tf=1, protocol=NaiveVoting,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True),
    SynchronousByzantine(5, 1, PossibleAdversaries[6],
                                        PossibleControllers[0], f=3, tf=3, protocol=DolevStrong_Wrong,
                                        measure=[ByzValidity,
                                                 ByzConsistency, ByzUnanimity],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=True, corrupt_sender=True),
    AsynchronousByzantine(3, 1, PossibleAdversaries[6],
                                        PossibleControllers[1], f=0, tf=0, protocol=Nakamoto,
                                        measure=[
                                                 ByzConsistency],
                                        centralized=False, centralized_adversary=PossibleAdversaries[
        0],
    has_sender=False, corrupt_sender=False,seed=None)
                                 ]
