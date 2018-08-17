
# Project Edelweiss (Work in Progress)

Edelweiss is a lightweight consensus protocol simulator.

For safer and better consensus protocols!

The program has been tested under python3.5 

## Goal

- Run and do vulnerability analysis existing consensus like [BOSCO](http://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/52180438.pdf),NaiveVoting,[DolevStrong](https://www.cs.huji.ac.il/~dolev/pubs/efficient-ba-no-auth.pdf),Herding in a straightforward way,you can see the
middle and final results of the running of the protocol and analysis the vulnerability of different protocols quickly.

- Provide a set of controllers,environments,settings,adversaries result measures and communication techniques so that you can easily implement and analysis your new consensus protocols without worring about the 'dirty work' of implementing it.

- Simulate the kinds of attacks that is theoretical possible but difficulty to achieve or observe in real distributed systems.

- Analysis the vulnerability of different protocols,say,change the parameters or weaken the assumptions of the protocols and see their performance

## File Description

### Infrastructure

| File | Description |
| --- | --- |
| [SynController.py](../master/src/Controllers/SynController.py) | Synchronous controller that controls the running of the protocol|

### Protocols

| File | Description |
| --- | --- |
| [DolevStrong.py](../master/src/Protocols/DolevStrong.py) | Synchronous DolevStrong protocol |
| [Herding.py](../master/src/Protocols/Herding.py) | Synchronous Herding protocol |
| [HerdingWithBroadcastFast.py](../master/src/Protocols/HerdingWithBroadcastFast.py) | Synchronous Herding protocol with broadcast |
| [NaiveVoting.py](../master/src/Protocols/NaiveVoting.py) | Synchronous NaiveVoting protocol |
| [DolevStrong_Wrong.py](../master/src/Protocols/DolevStrong_Wrong.py) | Uncorrectly written DolevStrong protocol |
| [BOSCO.py](../master/src/Protocols/BOSCO.py) | Synchronous BOSCO protocol |

### Adversaries

| File | Description |
| --- | --- |
| [CrashAdversary.py](../master/src/Adversaries/CrashAdversary.py) | Crash adversary |
| [HalfHalfSenderAdversary.py](../master/src/Adversaries/HalfHalfSenderAdversary.py) | Adversary that sends different msgs to different nodes|
| [SynBOSCOAgreementAttacker.py](../master/src/Adversaries/SynBOSCOAgreementAttacker.py) | Synchronous BOSCO agreement adversary |
| [SynBOSCOAgreementCentralizedAttacker.py](../master/src/Adversaries/SynBOSCOAgreementCentralizedAttacker.py)  | Synchronous BOSCO centralized agreement adversary|
| [SynHerdingAgreementFast.py](../master/src/Adversaries/SynHerdingAgreementFast.py) | Synchronous Herding advanced adversary|
| [SynHerdingBenchmarkAttacker.py](../master/src/Adversaries/SynHerdingBenchmarkAttacker.py) | Synchronous Herding brute-force adversary |
| [DolevStrongRoundAdversary.py](../master/src/Adversaries/DolevStrongRoundAdversary.py) |Synchronous DolevStong round adversary|


### Example Experiments

| File | Description |
| --- | --- |
| [HerdingStat.py](../master/src/ExperimentExample/HerdingStat.py) | Statistics vulnerability analysis on Herding |

## Getting Started

### Prerequisites

[Python3](https://www.python.org/getit/) \
[jsonpickle](https://github.com/jsonpickle/jsonpickle)

### Download

```sh
git clone git@github.com:FTRobbin/Edelweiss.git
```

### Usage

#### Run a demo experiment

Run the default experiment

```sh
python3 Main.py
```

Run a specific experiment

```sh
python3 Main.py -i experiment_num
```

experiment_num is the index of the experiment in variable demoProtocols in file [TestConfig.py](../master/src/Test/TestConfig.py) 

#### Do statistics analysis on Herding

```sh
python3 stat.py
```

Result is in the file HerdingStat.txt under directory [Edelweiss/src](../master/src) 

#### Test

To test all the protocols,run

```sh
python3 test.py
```

To test a specific protocol,run

```sh
python3 test.py -i protocol_num
```

proticol_num is the index of the prototol in variable TestProtocolsList in file [TestConfig](../master/src/Test/TestConfig.py) 

---

[Chujun Song](https://github.com/SongChujun), [Haobin Ni](https://github.com/FTRobbin), 2018
