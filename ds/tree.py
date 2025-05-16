from collections import defaultdict
from dataclasses import dataclass, field
from typing import List
import torch

@dataclass
class SpiralNode:
    node_id: int
    parent_id: int = -1 
    token_id: int
    
    trans_prob: float = 0.0
    
    depth: int = 0
    score: float = 1
    children: List[int] = field(default_factory=list)
    
def modify_node_info(node: SpiralNode, info_dict: dict):
    for key, value in info_dict.items():
        setattr(node, key, value)
    
class SpiralTree:
    def __init__(self, device, start_id=-1):
        self.id_to_node = {}
        self.depth_to_ids = defaultdict(list)
        
        self.root_id = start_id
        self.curr_gen_id = -1
        self.device = device
        
    def get_next_gen_id(self):
        self.curr_gen_id += 1
        return self.curr_gen_id
    
    def add_node(self, node: SpiralNode):
        '''
        Node you add should contain its own id, parent id, token id
        and trans_prob
        depth, score and children will be updated here
        '''
        if self.root_id == -1:
            self.root_id = node.node_id
            self.id_to_node[node.node_id] = node
            self.depth_to_ids[node.depth].append(node.node_id)
            return
            
        node.depth = self.id_to_node[node.parent_id].depth + 1
        node.score = self.id_to_node[node.parent_id].score * node.trans_prob
        self.id_to_node[node.node_id] = node
        self.depth_to_ids[node.depth].append(node.node_id)
        self.id_to_node[node.parent_id].children.append(node.node_id)
        
    def rebase_tree(self, new_root_id):
        if new_root_id not in self.id_to_node.keys():
            raise ValueError(f"New root id {new_root_id} not in tree")
        
        new_tree = SpiralTree(self.device)
        
        def dfs_and_append(node_id, parent_id=-1):
            if new_tree.root_id == -1:
                # Create a new node rather than modifying the original
                orig_node = self.id_to_node[new_root_id]
                new_node_id = new_tree.get_next_gen_id()
                
                new_node = SpiralNode(
                    node_id=new_node_id,
                    parent_id=-1,
                    token_id=orig_node.token_id,
                    trans_prob=0.0,
                    depth=0,
                    score=1
                )
                new_tree.add_node(new_node)
                
                # Store mapping from original ID to new ID for children
                id_mapping = {new_root_id: new_node_id}
                
                if not orig_node.children:
                    return id_mapping
                
                for child_id in orig_node.children:
                    child_mapping = dfs_and_append(child_id, parent_id=new_node_id)
                    id_mapping.update(child_mapping)
                    
                return id_mapping
            else:
                orig_node = self.id_to_node[node_id]
                new_node_id = new_tree.get_next_gen_id()
                
                new_node = SpiralNode(
                    node_id=new_node_id,
                    parent_id=parent_id,
                    token_id=orig_node.token_id,
                    trans_prob=orig_node.trans_prob
                )
                new_tree.add_node(new_node)
                
                # Store mapping from original ID to new ID
                id_mapping = {node_id: new_node_id}
                
                if not orig_node.children:
                    return id_mapping
                
                for child_id in orig_node.children:
                    child_mapping = dfs_and_append(child_id, parent_id=new_node_id)
                    id_mapping.update(child_mapping)
                    
                return id_mapping
        
        # Start the DFS from the new root
        dfs_and_append(new_root_id)
        return new_tree
    
    
            
    