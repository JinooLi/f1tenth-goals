import numpy as np
from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass

class LineType(Enum):
    """커브의 방향을 나타내는 열거형 클래스.
    Args:
        UNKNOWN (Enum): 무슨 방향 커브인지 모를 때
        LEFT (Enum): 왼쪽 커브인 경우
        RIGHT (Enum): 오른쪽 커브인 경우
    """
    UNKNOWN = -1
    LEFT = 0
    RIGHT = 1

class MapLineData(ABC):
    """맵의 라인 데이터를 추상화한 클래스. 이 클래스는 맵의 라인 데이터를 가져오는 함수를 제공한다.
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
class VerLineData:
    """수직선의 데이터를 저장하는 클래스. 자료형은 numpy.ndarray이며, 이것의 형식은 다음과 같아야 한다.  
    [ [ [left_x1, left_y1], [right_x1, right_y1] ], ... ]  
    각 좌표는 수직선의 양 끝 점이다. 각 원소는 float형이다.
    """
    coordinate: np.ndarray = None # type: ignore

class Node(ABC):
    """노드의 정보를 추상화한 클래스
    """
    @abstractmethod
    def __init__(self):
        """
        이 init함수는 노드를 무엇을 기준으로 만들 것인지를 지정한다.
        반드시 수직선 데이터(VerLineData)를 받아야 한다.
        """
        pass

    @abstractmethod
    def get_node(self)->np.ndarray:
        """수직선의 데이터를 받아 노드를 만든다.

        Returns:
            np.ndarray: 노드의 데이터
        """
        pass