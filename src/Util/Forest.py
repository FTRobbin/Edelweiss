from Util.Util import *

class Forest:
    def __init__(self, trees):
        self.trees = trees

    def insert(self, block):
        for tree in self.trees:
            if tree.insert_up(block):
                for other_tree in self.trees:
                    if other_tree == tree:
                        continue
                    if other_tree.insert_down(tree.clone()):
                        self.trees.remove(tree)
                        return
                return
        for tree in self.trees:
            if tree.insert_down(Tree(block.clone(),set())):
                return
        self.trees.add(Tree(block.clone(), set()))

    def get_forest_tail(self):
        return self.get_depthest_tree().get_tree_tail()
    
    def get_longest_chain(self):
        return self.get_depthest_tree().get_longest_chain()
    
    
    def get_depthest_tree(self):
        return max(self.trees, key=lambda x: (x.get_depth(),-x.node.get_id()))



class Tree:
    def __init__(self, node, subtree,depth=1):
        if not node:
            raise RuntimeError
        self.node = node
        self.subtree = subtree
        self.depth = depth
    


    def insert_down(self,insert_tree):
        insert_tree_node=insert_tree.get_node()
        if self.node == insert_tree_node: 
            return True
        if insert_tree_node.check_is_previous(self.node.get_id()):
            for tree in self.subtree:
                if tree.node.get_id()==insert_tree.node.get_id():
                    return True
            self.subtree.add(insert_tree.clone())
            self.depth=max(self.depth,insert_tree.get_depth()+1)
            return True
        if not self.subtree:
            return False
        for tree in self.subtree:
            if tree.insert_down(insert_tree):
                self.depth = max(tree.get_depth()+1,self.depth)
                return True
        return False



    def insert_up(self, block):
        if self.node.check_is_previous(block.get_id()):
            new_subtree = {self.clone()}
            self.node = block.clone()
            self.subtree = new_subtree
            self.depth += 1
            return True
        return False

    def clone(self):
        if not self.node:
            raise RuntimeError
        if not self.subtree:
            return Tree(self.node.clone(), set())
        new_node = self.node.clone()
        new_subtree = set()
        for tree in self.subtree:
            new_subtree.add(tree.clone())
        return Tree(new_node, new_subtree,self.depth)

    def get_depth(self):
        return self.depth

    def get_tree_tail(self):
        if not self.subtree:
            return self
        return self.get_depthest_subtree().get_tree_tail()

    def get_node(self):
        return self.node

    def get_subtree(self):
        return self.subtree

    def get_longest_chain(self):
        if not self.subtree:
            return [self.node]
        return [self.node]+self.get_depthest_subtree().get_longest_chain()
    
    
    def get_depthest_subtree(self):
        return max(self.subtree, key=lambda x: (x.get_depth(),-x.node.get_id()))