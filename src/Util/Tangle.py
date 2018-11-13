from random import shuffle
from random import uniform
from random import randint
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

    def random_walk(self):
        walker_list = []
        walker_start_point_list = []
        selected_tip = []
        for i in range(self.walker_num):
            walker_start_point_list.append(self.genesis_site)
            walker_list.append(self.genesis_site)
        while(True):
            walking_order = [i for i in range(len(walker_list))]
            shuffle(walking_order)
            to_be_deleted_walker = []
            for i in walking_order:
                if not walker_list[i].children_list:
                    if not selected_tip:
                        selected_tip.append(walker_list[i])
                        to_be_deleted_walker.append(walker_list[i])
                        continue
                    else:
                        if selected_tip[0].vote != walker_list[i].vote:
                            del selected_tip[0]
                            walker_list.append(self.genesis_site)
                            walker_list[i] = self.genesis_site
                            continue
                        else:
                            selected_tip.append(walker_list[i])
                            return selected_tip

                transition_probability_list = self.calculate_transition_probability(
                    walker_start_point_list[i], walker_list[i])
                cumulative_probability_list = list(reduce(lambda result, x: iadd(
                    result, [result[-1] + x]), transition_probability_list, [0])[1:])
                sum = reduce(lambda a, b: a+b, transition_probability_list)
                random_point = randint(1, sum)
                for j in range(len(cumulative_probability_list)):
                    if random_point <= cumulative_probability_list[j]:
                        walker_list[i] = walker_list[i].children_list[j]
                        if not walker_list[i].children_list:
                            if not selected_tip:
                                selected_tip.append(walker_list[i])
                                to_be_deleted_walker.append(walker_list[i])
                                break
                            else:
                                if selected_tip[0].vote != walker_list[i].vote:
                                    del selected_tip[0]
                                    walker_list.append(self.genesis_site)
                                    break
                                else:
                                    selected_tip.append(walker_list[i])
                                    return selected_tip
                        break

            for walker in to_be_deleted_walker:
                walker_list.remove(walker)

    def calculate_transition_probability(self, start_point, walker):
        cumulative_weight_list = []
        for child in walker.children_list:
            cumulative_weight_list.append(child.calculate_cumulative_weight())
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
        ratio_dict = {}
        for k, v in layer_dict.items():
            count_list = [0, 0]
            for i in range(len(v)):
                if v[i].vote != 0 and v[i].vote != 1:
                    continue
                count_list[v[i].vote] = count_list[v[i].vote]+1
            sum = count_list[0]+count_list[1]
            if sum != 0:
                count_list[0] = count_list[0]*1.0/sum
                count_list[1] = count_list[1]*1.0/sum
            for i in range(len(v)):
                v[i] = v[i].id
            ratio_dict[k] = count_list
        print(layer_dict)
        print(ratio_dict)


class Tangle_Site:
    current_id = 4

    def __init__(self, father_id_list, children_list, miner, vote, id=None):
        if id == None:
            self.id = Tangle_Site.current_id
            Tangle_Site.current_id = Tangle_Site.current_id+1
            self.father_id_list = father_id_list
            self.children_list = children_list
            self.miner = miner
            self.vote = vote
        else:
            self.id = id
            self.father_id_list = father_id_list
            self.children_list = children_list
            self.miner = miner
            self.vote = vote

    @staticmethod
    def get_genesis_site():
        genesis_site = Tangle_Site([], [], None, None, 1)
        return genesis_site

    def calculate_cumulative_weight(self):
        # len(self.calculate_descendants_helper())
        return len(self.calculate_descendants_helper())

    def calculate_descendants_helper(self):
        visited = []
        descendant_set = set()
        self.calculate_descendants(visited, descendant_set)
        return descendant_set

    def calculate_descendants(self, visited, descendant_set):
        if self.id in visited:
            return
        visited.append(self.id)
        descendant_set.add(self.id)
        if not self.children_list:
            return
        for child in self.children_list:
            child.calculate_descendants(visited, descendant_set)

    def find_site_with_id_helper(self, id, visited, site):
        if self.id in visited:
            return
        visited.append(self.id)
        if self.id == id:
            site[0] = self
            return
        if not self.children_list:
            return
        for child in self.children_list:
            child.find_site_with_id_helper(id, visited, site)
            if site[0]:
                return
        return

    def find_site_with_id(self, id):
        visited = []
        site = [None]
        self.find_site_with_id_helper(id, visited, site)
        return site[0]

    def clone(self):
        return Tangle_Site(self.father_id_list.copy(), [], self.miner, self.vote, self.id)

    def copy(self):
        return self.clone()

    def check_site_present_helper(self, site, visited, present):
        if self.id in visited:
            return
        visited.append(self.id)
        if self.id == site.id:
            present[0] = True
            return
        if not self.children_list:
            return
        for child in self.children_list:
            child.check_site_present_helper(site, visited, present)
            if present[0]:
                return
        return
    

    def check_site_present(self, site):
        visited = []
        present = [False]
        self.check_site_present_helper(site, visited, present)
        return present[0]

    def check_identical_site(self, another_site):
        if self.id != another_site.id:
            return False
        if self.father_id_list != another_site.father_id_list:
            return False
        if not self.children_list:
            if not another_site.children_list:
                return True
            return False
        mychildren_dict = {}
        for child in self.children_list:
            mychildren_dict[child.id] = child
        hischildren_dict = {}
        for child in another_site.children_list:
            hischildren_dict[child.id] = child
        if len(mychildren_dict) != len(hischildren_dict):
            return False
        for k, v in mychildren_dict.items():
            if k not in hischildren_dict.keys():
                return False
            if not v.check_identical_site(hischildren_dict[k]):
                return False
        return True

    def get_sender(self):
        return self.miner
