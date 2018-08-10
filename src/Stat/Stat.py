import random
from Util.Util import *

def stat(setting,input,f,tf,_lambda,times):
    setting.set_input(input)
    setting.set_n(len(input))
    setting.set_f(f)
    setting.set_tf(tf)
    setting.set_lambda(_lambda)
    stat_dict = {'Consistency': 0, 'Validity': 0, 'Unanimity': 0}
    for i in range(times):
        setting.set_seed(i)
        random.shuffle(input)
        res = run_and_get_result(setting)
        for k, v in stat_dict.items():
            if not res[k]:
                stat_dict[k] = v+1
    for k,v in stat_dict.items():
        stat_dict[k]=v/times
    print(stat_dict)