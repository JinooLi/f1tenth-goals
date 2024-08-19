import numpy as np
from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass

class LineType(Enum):
    UNKNOWN = -1
    LEFT = 0
    RIGHT = 1

class MapLineData(ABC):
    """맵의 라인 데이터를 추상화한 클래스
    """
    @abstractmethod
    def __init__(self):
        """__init__ 함수에서 맵을 데이터를 받아오거나 초기화한다.
        """
        pass
    
    @abstractmethod
    def get_left_line(self)->np.ndarray:
        """이 함수에서 왼쪽 라인을 배열을 반환한다.

        Returns:
            np.ndarray: 왼쪽 라인의 데이터
        """
        pass
    
    @abstractmethod
    def get_right_line(self)->np.ndarray:
        """이 함수에서 오른쪽 라인을 배열을 반환한다.

        Returns:
            np.ndarray: 오른쪽 라인의 데이터
        """
        pass
    
    @abstractmethod
    def get_left_mod_index(self, index:int)->int:
        """이 함수에서 왼쪽 라인의 인덱스를 받아\n
        왼쪽 라인의 절대적인 인덱스를 반환한다.

        Args:
            index (int): 범위를 벗어나는 정수여도 상관 없다.

        Returns:
            int: 왼쪽 라인의 절대적인 인덱스
        """
        pass
    
    @abstractmethod
    def get_right_mod_index(self, index:int)->int:
        """이 함수에서 오른쪽 라인의 인덱스(범위를 벗어나든 음수이든 상관 없다.)를 받아\n
        오른쪽 라인의 절대적인 인덱스를 반환한다.

        Args:
            index (int): 범위를 벗어나는 정수여도 상관 없다.

        Returns:
            int: 오른쪽 라인의 절대적인 인덱스
        """
        pass

@dataclass
class VirLineData:
    """수직선의 데이터를 저장하는 클래스. 자료형은 numpy.ndarray이며, 이것의 형식은 다음과 같아야 한다.  
    [ [ [left_x1, left_y1], [right_x1, right_y1] ], ...]  
    각 좌표는 수직선의 양 끝 점이다. 각 원소는 float형이다.
    """
    coordinate: np.ndarray = None

class Node(ABC):
    """노드의 정보를 추상화한 클래스
    """
    def __init__(self,
                  node_pos_num_per_ver_line:int, 
                  dir_num:int,
                  speed_num:int):
        """노드의 정보를 지정하는 클래스

        Args:
            node_pos_num_per_ver_line (int): 한 라인 위에 가질 수 있는 노드 위치의 개수
            dir_num (int): 한 위치에서 가질 수 있는 노드 방향의 개수
            speed_num (int): 한 방향에서 가질 수 있는 노드 속력의 개수
        """
        self.node_pos_num_per_ver_line = node_pos_num_per_ver_line
        self.dir_num = dir_num
        self.speed_num = speed_num
        self.node_num = node_pos_num_per_ver_line * dir_num * speed_num
    
    @abstractmethod
    def make_node(self, vir_line_data:VirLineData)->np.ndarray:
        """수직선의 데이터를 받아 노드를 만든다.

        Args:
            vir_line_data (VirLineData): 수직선의 데이터

        Returns:
            np.ndarray: 노드의 데이터
        """
        pass