from core.definition import VirLineData, Node
import numpy as np

class PointMassNode(Node):
    """질량점 노드의 데이터를 생성하는 클래스.  
    이 클래스는 NodeInfo 클래스를 상속받아 구현되었다.
    """

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