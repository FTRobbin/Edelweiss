from Util.Util import Tangle_Site
from random import shuffle
from random import uniform
from functools import reduce
from operator import iadd
import queue

class Tangle:
    def __init__(self, genesis_site, walker_num):
        self.genesis_site = genesis_site
        self.walker_num = walker_num
    
    @staticmethod
    def init_with_fork():
        fork_tangle = Tangle(Tangle_Site.get_genesis_site(),
                             2)
        site2 = Tangle_Site([1], [], None, 1, 2)
        site3 = Tangle_Site([1], [], None, 0, 3)
        fork_tangle.insert_site(site2)
        fork_tangle.insert_site(site3)
        return fork_tangle

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
        self.simple_print()
        return self.genesis_site.check_identical_site(another_tangle.genesis_site)
    
    
    def simple_print(self):
        q = queue.Queue()
        q.put(self.genesis_site)
        visited = {self.genesis_site}
        layer_dict = {0: [self.genesis_site]}
        depth_dict = {self.genesis_site.id: 0}
        while(not q.empty()):
            current_site = q.get()
            if not current_site.children_list:
                continue
            for child in current_site.children_list:
                if not child in visited:
                    visited.add(child)
                    q.put(child)
                    if (depth_dict[current_site.id]+1) not in layer_dict.keys():
                        layer_dict[depth_dict[current_site.id]+1] = []
                    depth_dict[child.id] = depth_dict[current_site.id]+1
                    layer_dict[depth_dict[current_site.id]+1].append(child)
        ratio_dict={}
        for k,v in layer_dict.items():
            count_list=[0,0]
            for i in range(len(v)):
                if v[i].vote!=0 and v[i].vote!=1:
                    continue
                count_list[v[i].vote]=count_list[v[i].vote]+1
            sum = count_list[0]+count_list[1]
            if sum!=0:
                count_list[0]=count_list[0]*1.0/sum
                count_list[1]=count_list[1]*1.0/sum
            for i in range(len(v)):
                v[i]=v[i].id
            ratio_dict[k]=count_list
        print(layer_dict)
        print(ratio_dict)
