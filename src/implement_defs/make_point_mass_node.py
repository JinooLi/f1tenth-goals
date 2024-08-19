from core.definition import VirLineData, Node
import numpy as np

class PointMassNode(Node):
    """질량점 노드의 데이터를 생성하는 클래스.  
    이 클래스는 Node 클래스를 상속받아 구현되었다.
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

    def get_node(self, vir_line_data:VirLineData) -> np.ndarray: # type: ignore
        """노드의 정보와 수직선들을 이용하여 노드를 만들고 반환하는 함수    

        Args:
            node_info (NodeInfo): 만들 노드의 정보를 담은 클래스
            vir_line_index (np.ndarray): 수직선들의 왼쪽 점과 오른쪽 점의 index를 담은 배열.

        Returns:
            np.ndarray:수직선별 노드들의 정보를 담은 배열.\n
            [ \n
                [[x축 위치11, y축 위치11, x축 속도11, y축 속도11], [x축 위치12, y축 위치12, x축 속도12, y축 속도12],...],\n
                [[x축 위치21, y축 위치21, x축 속도21, y축 속도21], [x축 위치22, y축 위치22, x축 속도22, y축 속도22],...],\n
            ]
        """
        pass