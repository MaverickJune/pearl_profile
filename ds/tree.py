from collections import defaultdict
from dataclasses import dataclass, field
from typing import List
import torch

@dataclass
class SpiralNode:
    node_id: int
    parent_id: int 
    token_id: int
    
    trans_prob: float
    
    depth: int = -1
    score: float = -1
    children: List[int] = field(default_factory=list)
    
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
        node.depth = self.id_to_node[node.parent_id].depth + 1
        node.score = self.id_to_node[node.parent_id].score * node.trans_prob
        self.id_to_node[node.node_id] = node
        self.depth_to_ids[node.depth].append(node.node_id)
        self.id_to_node[node.parent_id].children.append(node.node_id)
        
    
    