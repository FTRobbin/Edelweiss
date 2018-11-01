from Util import *
from random import shuffle
from random import uniform
from functools import reduce
from operator import iadd


class Tangle:
    def __init__(self, genesis_site, walker_num):
        self.genesis_site = genesis_site
        self.walker_num = walker_num

    def get_tobeapproved_site(self):
        return self.random_walk()

    def random_walk(self):
        walker_list = []
        walker_start_ponit_list = []
        selected_tip = []
        for i in range(self.walker_num):
            walker_start_ponit_list.append(self.genesis_site)
            walker_list.append(self.genesis_site)
        while(True):
            walking_order = [i for i in range(len(walker_list))]
            shuffle(walking_order)
            to_be_deleted_walker=[]
            for i in walking_order:
                if not walker_list[i].children_list:
                    selected_tip.append(walker_list[i])
                    to_be_deleted_walker.append(walker_list[i])
                    if len(selected_tip) == 2:
                        return selected_tip
                    continue
                transition_probability_list = self.calculate_transition_probability(
                    walker_start_ponit_list[i], walker_list[i])
                # calculate cumulative sum of transition_probability_list
                cumulative_probability_list = list(reduce(lambda result, x: iadd(
                    result, [result[-1] + x]), transition_probability_list, [0])[1:])
                random_point = uniform(0, 1)
                for j in range(len(cumulative_probability_list)):
                    if random_point < cumulative_probability_list[j]:
                        walker_list[i] = walker_list[i].children_list[j-1]
                        if not walker_list[i].children_list:
                            selected_tip.append(walker_list[i])
                            to_be_deleted_walker.append(walker_list[i])
                            if len(selected_tip) == 2:
                                return selected_tip
                        break
            for walker in to_be_deleted_walker:
                walker_list.remove(walker)

    def calculate_transition_probability(self, start_point, walker):
        cumulative_weight_list = []
        for child in walker.children_list:
            cumulative_weight_list.append(child.calculate_cumulative_weight())
        sum = reduce(lambda a, b: a+b, cumulative_weight_list)
        for i in range(len(cumulative_weight_list)):
            cumulative_weight_list[i] = cumulative_weight_list[i]/sum
        return cumulative_weight_list

    def check_site_present(self, site):
        return self.genesis_site.check_site_present(site)

    def insert_site(self, site):
        if self.check_site_present(site):
            return
        for father_id in site.father_id_list:
            father_site = self.genesis_site.find_site_with_id(father_id)
            if not father_site:
                raise RuntimeError
            father_site.children_list.append(site)
    def check_identical(self, another_tangle):
        return self.genesis_site.check_identical_site(another_tangle.genesis_site)
