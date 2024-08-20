from core.definition import VerLineData, Node
import numpy as np

class PointMassNode(Node):
    """점질량 노드의 데이터를 생성하는 클래스.  
    이 클래스는 Node 클래스를 상속받아 구현되었다.
    """
    def __init__(self,
                  ver_line_data:VerLineData,
                  node_pos_num_per_ver_line:int = 5, 
                  dir_num:int = 5,
                  speed_num:int = 5,
                  maximum_speed:float = 1.0):
        """노드의 정보를 지정하는 클래스

        Args:
            ver_line_data (VerLineData): 수직선의 데이터를 담은 클래스
            node_pos_num_per_ver_line (int): 한 라인 위에 가질 수 있는 노드 위치의 개수 (기본 값: 5)
            dir_num (int): 한 위치에서 가질 수 있는 노드의 방향 개수 (기본 값: 5)
            speed_num (int): 한 방향에서 가질 수 있는 노드 속력의 개수 (기본 값: 5)
            maximum_speed (float): 노드의 최대 속력 (기본 값: 1.0)
        """
        # init
        self.ver_line_data = ver_line_data
        self.node_pos_num_per_ver_line = node_pos_num_per_ver_line
        self.dir_num = dir_num
        self.speed_num = speed_num
        self.maximum_speed = maximum_speed
        # 점 질량은 속력이 0인 경우는 방향이 상관 없으므로 방향에 상관 없이 하나의 노드로 친다.
        self.node_num = node_pos_num_per_ver_line * (dir_num * (speed_num - 1) + 1)  

        # 노드를 만든다.
        self.node = self.make_node()
    
    def get_node(self)->np.ndarray:
        """노드를 반환하는 함수    
        Returns:
            np.ndarray:수직선별 노드들의 정보를 담은 배열.\n
            [ \n
                [[x축 위치11, y축 위치11, x축 속도11, y축 속도11], [x축 위치12, y축 위치12, x축 속도12, y축 속도12],...],\n
                [[x축 위치21, y축 위치21, x축 속도21, y축 속도21], [x축 위치22, y축 위치22, x축 속도22, y축 속도22],...],\n
            ]
        """
        return self.node
    
    def get_node_index_on_a_line(self,
                       pos_index:int,
                       dir_index:int,
                       speed_index:int)->int:
        """원하는 노드의 인덱스를 반환하는 함수  

        Args:
            pos_index (int): 수직선 위의 위치 인덱스  
            dir_index (int): 방향 인덱스  
            speed_index (int): 속력 인덱스  
            
        Returns:
            int: 원하는 노드의 인덱스
        """
        if speed_index == 0:
            return pos_index * (self.dir_num * (self.speed_num - 1) + 1)
        return pos_index * (self.dir_num * (self.speed_num - 1) + 1) + dir_index * (self.speed_num - 1) + speed_index

    def make_node(self) -> np.ndarray:
        """노드를 만들고 반환하는 함수    
        Returns:
            np.ndarray:수직선별 노드들의 정보를 담은 배열.\n
            [ \n
                [[x축 위치11, y축 위치11, x축 속도11, y축 속도11], [x축 위치12, y축 위치12, x축 속도12, y축 속도12],...],\n
                [[x축 위치21, y축 위치21, x축 속도21, y축 속도21], [x축 위치22, y축 위치22, x축 속도22, y축 속도22],...],\n
            ]
        """

        ver_line_coord = self.ver_line_data.coordinate
        node = np.zeros((len(ver_line_coord), self.node_num, 4), dtype=np.float32)
        rad_per_dir:float = np.pi / (self.dir_num + 1)
        for i in range(len(ver_line_coord)):# 모든 수직선에 대한 노드 계산
            for n in range(self.node_pos_num_per_ver_line): # 하나의 수직선에 대한 노드 계산
                # 수직선의 양 끝점을 이용하여 노드의 위치를 계산한다.
                pos_x:float = (ver_line_coord[i][0][0] * (self.node_pos_num_per_ver_line - n) \
                            + ver_line_coord[i][1][0] * (1 + n)) / (self.node_pos_num_per_ver_line + 1)
                pos_y:float = (ver_line_coord[i][0][1] * (self.node_pos_num_per_ver_line - n) \
                            + ver_line_coord[i][1][1] * (1 + n)) / (self.node_pos_num_per_ver_line + 1)
                # 속도가 0인 경우의 노드
                posindex = n * (self.dir_num * (self.speed_num - 1) + 1)
                node[i][posindex][0] = pos_x
                node[i][posindex][1] = pos_y
                node[i][posindex][2] = 0
                node[i][posindex][3] = 0

                # 방향에 따른 단위 벡터를 구한다.
                # 오른쪽으로부터 반시계방향으로 방향을 지정한다.
                # 우선 왼쪽 점에서 시작해 오른쪽 점으로 가는 벡터를 구한다.
                vec:np.ndarray = ver_line_coord[i][1] - ver_line_coord[i][0]
                # 정규화한다.
                vec = vec / np.linalg.norm(vec)
                for j in range(self.dir_num): # 하나의 위치에 대한 노드 계산
                    # 회전행렬을 이용하여 방향을 구한다.
                    rotate:np.ndarray = np.array([[np.cos(rad_per_dir*(j+1)),-np.sin(rad_per_dir*(j+1))],\
                                                [np.sin(rad_per_dir*(j+1)), np.cos(rad_per_dir*(j+1))]])
                    rotate_vec:np.ndarray = np.dot(rotate, vec)
                    dirindex = j * (self.speed_num - 1)
                    for k in range(1, self.speed_num): # 하나의 방향에 대한 노드 계산
                        speedindex = posindex + dirindex + k
                        node[i][speedindex][0] = pos_x
                        node[i][speedindex][1] = pos_y
                        node[i][speedindex][2] = rotate_vec[0] * self.maximum_speed * (k/self.speed_num)
                        node[i][speedindex][3] = rotate_vec[1] * self.maximum_speed * (k/self.speed_num)
        
        return node