PossibleControllers = [SynByzController]
PossibleAdversaries = [CrashAdversary, HalfHalfSenderAdversary,
                       SynBOSCOValidityAttacker, SynBOSCOValidityCentralizedAttacker, SynHerdingValidityAttacker]
TestProtocolsList=[NaiveVoting,DecentralizedBosco,DecentralizedBoscoValidityAttack,DecentralizedBoscoValidityAttack,
CentralizedBosco.CentralizedBoscoValidityAttack,DolevStrong,Herding,HerdingValidityAttack]
NaiveVoting=[SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                                    PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                    measure=[ByzValidity,
                                                             ByzConsistency, ByzUnanimity],
                                                    centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),#1
    SynchronousByzantine(10, 0, PossibleAdversaries[2],
                                                    PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                    measure=[ByzValidity,
                                                             ByzConsistency, ByzUnanimity],
                                                    centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),#2

    SynchronousByzantine(5, 1, PossibleAdversaries[2],
                                                    PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                    measure=[ByzValidity,
                                                             ByzConsistency, ByzUnanimity],
                                                    centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),#3

    

    SynchronousByzantine(5, 0, PossibleAdversaries[2],
                                                    PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                    measure=[ByzValidity,
                                                             ByzConsistency, ByzUnanimity],
                                                    centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False),#4

    SynchronousByzantine(20, 1, PossibleAdversaries[2],
                                                    PossibleControllers[0], f=0, tf=0, protocol=NaiveVoting,
                                                    measure=[ByzValidity,
                                                             ByzConsistency, ByzUnanimity],
                                                    centralized=False, centralized_adversary=PossibleAdversaries[
    3],
    has_sender=True, corrupt_sender=False)]#5
    
    DecentralizedBosco=[SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                                measure=[ByzValidity,
                                                         ByzConsistency, ByzUnanimity],
                                                centralized=False, centralized_adversary=PossibleAdversaries[3])]
    DecentralizedBoscoValidityAttack= [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[2],
                                                              PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                              measure=[ByzValidity,
                                                                       ByzConsistency, ByzUnanimity],
                                                              centralized=False, centralized_adversary=PossibleAdversaries[3])]
    CentralizedBosco= [SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], PossibleAdversaries[3],
                                              PossibleControllers[0], f=3, tf=3, protocol=BOSCO,
                                              measure=[ByzValidity,
                                                       ByzConsistency, ByzUnanimity],
                                              centralized=True, centralized_adversary=PossibleAdversaries[3])]
    CentralizedBoscoValidityAttack =[SynchronousByzantine(10, [1, 1, 1, 0, 0, 0, 1, 1, 1, 1,
                                                                 ], PossibleAdversaries[3],
                                                            PossibleControllers[0], f=3, tf=4, protocol=BOSCO,
                                                            measure=[ByzValidity,
                                                                     ByzConsistency, ByzUnanimity],
                                                            centralized=True, centralized_adversary=PossibleAdversaries[3])]
    DolevStrong= [SynchronousByzantine(10, 1, PossibleAdversaries[2],
                                         PossibleControllers[0], f=0, tf=0, protocol=DolevStrong,
                                         measure=[ByzValidity,
                                                  ByzConsistency, ByzUnanimity],
                                         centralized=False, centralized_adversary=PossibleAdversaries[
        3],
        has_sender=True, corrupt_sender=False)]
    Herding = [SynchronousByzantine(10, [0, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                                          ], PossibleAdversaries[3],
                                     PossibleControllers[0], f=0, tf=0, protocol=Herding,
                                     measure=[ByzValidity,
                                              ByzConsistency, ByzUnanimity],
                                     centralized=False, centralized_adversary=PossibleAdversaries[3], seed=0, _lambda=3)]
    HerdingValidityAttack= [SynchronousByzantine(10, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], PossibleAdversaries[4],
                                                   PossibleControllers[0], f=5, tf=5, protocol=Herding,
                                                   measure=[ByzValidity,
                                                            ByzConsistency, ByzUnanimity],
                                                   centralized=False, centralized_adversary=PossibleAdversaries[3], seed=4, _lambda=4, k=4))

]