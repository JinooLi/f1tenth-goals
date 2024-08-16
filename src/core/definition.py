import numpy as np
from enum import Enum
from abc import ABC, abstractmethod

class LineType(Enum):
    UNKNOWN = -1
    LEFT = 0
    RIGHT = 1

class NodeInfo:
    def __init__(self,
                  node_pos_num_per_ver_line:int, 
                  dir_num:int,
                  speed_num:int):
        self.node_pos_num_per_ver_line = node_pos_num_per_ver_line
        self.dir_num = dir_num
        self.speed_num = speed_num
        self.node_num = node_pos_num_per_ver_line * dir_num * speed_num
    
    @abstractmethod
    def make_node():
        pass


class MapLineData(ABC):
    @abstractmethod
    def __init__(self):
        # 이 함수에서 맵을 데이터를 받아오거나 초기화한다.
        pass
    
    @abstractmethod
    def get_left_line(self)->np.ndarray:
        # 이 함수에서 왼쪽 라인을 배열을 반환한다.
        pass
    
    @abstractmethod
    def get_right_line(self)->np.ndarray:
        # 이 함수에서 오른쪽 라인을 배열을 반환한다.
        pass
    
    @abstractmethod
    def get_left_mod_index(self, index:int)->int:
        # 이 함수에서 왼쪽 라인의 인덱스(범위를 벗어나든 음수이든 상관 없다.)를 받아
        # 왼쪽 라인의 절대적인 인덱스를 반환한다.
        pass
    
    @abstractmethod
    def get_right_mod_index(self, index:int)->int:
        pass