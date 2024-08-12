import numpy as np
from enum import Enum
from abc import ABC, abstractmethod

class LineType(Enum):
    UNKNOWN = -1
    LEFT = 0
    RIGHT = 1

class NodeInfo(ABC):
    def __init__(self,
                  node_pos_num_per_ver_line:int, 
                  dir_num:int,
                  speed_num:int)->np.ndarray:
        self.node_pos_num_per_ver_line = node_pos_num_per_ver_line
        self.dir_num = dir_num
        self.speed_num = speed_num
        self.node_num = node_pos_num_per_ver_line * dir_num * speed_num
    
    @abstractmethod
    def make_node():
        pass