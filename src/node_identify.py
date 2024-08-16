import numpy as np
import matplotlib.pyplot as plt 
from core.definition import LineType, MapLineData
import make_sqare_map as map

    
class GridNodeMap:
    def __init__(self, 
                 map_data:MapLineData, 
                 line_div_num:int = 5, 
                 line_dist_index:int = 700
                 ):
        """
        맵을 나누는 수직선들을 만드는 클래스

        Args:
            map_data (MapLineData): 맵 정보를 담은 클래스
            line_div_num (int, optional): 수직선 위의 노드 개수. Defaults to 5.
            line_dist_index (int, optional): 수직선간 최대 거리(인덱스임). Defaults to 700.
        """
        self.map_data = map_data
        self.line_div_num = line_div_num
        self.line_dist_index = line_dist_index

    def get_grid_node(self) -> np.ndarray: # type: ignore
        pass

    def get_vir_line(self, left_start_index:int, right_start_index:int)->np.ndarray:
        """
        맵을 나누는 수직선들을 만드는 함수. 각각의 수직선들은 두 개의 점으로 이루어진다.

        Args:
            left_start_index (int): 왼쪽 라인의 시작 index
            right_start_index (int): 오른쪽 라인의 시작 index

        Returns:
            vir_line_index (np.ndarray): 수직선들의 왼쪽 점과 오른쪽 점의 index를 담은 배열.
            [ [ left point index1, right point index1 ], [ ~2, ~2 ], ... ]
        """
        class LeftRigt:
            def __init__(self):
                self.line:np.ndarray
                self.start_index:int
        
        left = LeftRigt()
        right = LeftRigt()

        left.start_index = left_start_index
        right.start_index = right_start_index

        left.line = self.map_data.get_left_line()
        right.line = self.map_data.get_right_line()

        # 처음 수직선을 그릴 기준점을 정한다.
        # 이때, 오른쪽 커브인지 외쪽 커브인지 판단한다.
        # 오른쪽 커브인 경우, 왼쪽 점을 기준으로 수직선을 그린다. 반대는 오른쪽 점으로 한다.

        flag:LineType = LineType.UNKNOWN
        if self.is_left_curve(left_index = left_start_index, right_index = right_start_index, detect_range= self.line_dist_index):  
            right_start_abs_index = self.map_data.get_right_mod_index(right_start_index)
            right_start_point:np.ndarray = right.line[right_start_abs_index]

            min_norm_left_index:int = left_start_index
            abs_index = self.map_data.get_left_mod_index(min_norm_left_index)
            min_norm:float = float(np.linalg.norm(left.line[abs_index] - right_start_point))

            for i in range(2 * self.line_dist_index): # 왼쪽 라인의 점들 중에서 가장 가까운 점을 찾는다. 이때 앞뒤로 line_dist_index 개 안에서 찾는다.
                left_index = left_start_index - self.line_dist_index + i
                left_abs_index = self.map_data.get_left_mod_index(left_index)
                norm:float = np.linalg.norm(left.line[left_abs_index] - right_start_point)  # type: ignore
                if norm < min_norm:
                    min_norm = norm
                    min_norm_left_index = left_index
            
            vir_line_index = np.array([[min_norm_left_index, right_start_index]], dtype=int)
            flag = LineType.RIGHT
        else: # 위와 같은 방법으로 오른쪽 커브인 경우.
            left_start_abs_index = self.map_data.get_left_mod_index(left_start_index)
            left_start_point:np.ndarray = left.line[left_start_abs_index]

            min_norm_right_index:int = right_start_index
            abs_index = self.map_data.get_right_mod_index(min_norm_right_index)
            min_norm:float = np.linalg.norm(right.line[abs_index] - left_start_point) # type: ignore

            for i in range(2 * self.line_dist_index):
                right_index = right_start_index - self.line_dist_index + i
                right_abs_index = self.map_data.get_right_mod_index(right_index)
                norm:float = np.linalg.norm(right.line[right_abs_index] - left_start_point) # type: ignore
                if norm < min_norm:
                    min_norm = norm
                    min_norm_right_index = right_index
            
            vir_line_index = np.array([[left_start_index, min_norm_right_index]], dtype=int)
            flag = LineType.LEFT

        # 나머지 수직선들을 그린다.
        left_line_len:int = len(left.line)
        right_line_len:int = len(right.line)
        left_index:int = vir_line_index[0][0]
        right_index:int = vir_line_index[0][1]
        while True:
            if flag == LineType.RIGHT: # 오른쪽 라인을 기준으로 왼쪽 라인을 찾는다.
                # 다음 수직선의 오른쪽 점을 가리키는 index를 구한다.
                right_index += self.line_dist_index
                
                if right_index - vir_line_index[0][1] >= right_line_len:
                    break # 오른쪽 라인의 끝에 도달하면 종료
                
                # 가장 가까운 점을 구하기 위한 초기화
                right_abs_index = self.map_data.get_right_mod_index(right_index)
                right_point:np.ndarray = right.line[right_abs_index]

                left_abs_index = self.map_data.get_left_mod_index(left_index)
                min_norm:float = np.linalg.norm(right_point - left.line[left_abs_index]) # type: ignore
                min_norm_left_index:int = left_index

                for i in range(2*self.line_dist_index):
                    index = left_index + i
                    abs_index = self.map_data.get_left_mod_index(index)
                    norm:float = np.linalg.norm(right_point - left.line[abs_index]) # type: ignore

                    if norm < min_norm:
                        min_norm = norm
                        min_norm_left_index = index

                left_index = min_norm_left_index
                vir_line_index = np.append(vir_line_index, [[left_index, right_index]], axis=0)

            else:
                left_index += self.line_dist_index

                if left_index - vir_line_index[0][0] >= left_line_len:
                    break

                left_abs_index = self.map_data.get_left_mod_index(left_index)
                left_point:np.ndarray = left.line[left_abs_index]

                right_abs_index = self.map_data.get_right_mod_index(right_index)
                min_norm:float = np.linalg.norm(left_point - right.line[right_abs_index]) # type: ignore
                min_norm_right_index:int = right_index

                for i in range(2*self.line_dist_index):
                    index = right_index + i
                    abs_index = self.map_data.get_right_mod_index(index)
                    norm = np.linalg.norm(left_point - right.line[abs_index]) # type: ignore

                    if norm < min_norm:
                        min_norm = norm
                        min_norm_right_index = index
                
                right_index = min_norm_right_index
                vir_line_index = np.append(vir_line_index, [[left_index, right_index]], axis=0)
            
            # 다음 기준점을 판단하기 위해 만든 수직선 앞의 트랙이 어떤 커브인지 판단한다.
            if self.is_left_curve(left_index + self.line_dist_index,\
                                right_index + self.line_dist_index,\
                                int(1.1*self.line_dist_index)): 
                # 여기서 detect_range는 1.1*self.line_dist_index로 설정한다.
                # 딱 line_dist_index만큼만 설정하면 코너에서 어떤 커브인지 오판할 수 있기 때문이다.
                flag = LineType.RIGHT
            else:
                flag = LineType.LEFT

        return vir_line_index
    
    def is_left_curve(self, left_index:int, right_index:int, detect_range:int = 100)->bool:
        """index번째 점을 기준으로 detect_range만큼의 점을 이용하여 
        왼쪽 커브인지 오른쪽 커브인지 판단하는 함수.

        Args:
            left_index (int): 왼쪽 라인 점의 index
            right_index (int): 오른쪽 라인 점의 index
            detect_range (int, optional): 고려할 기준점 앞뒤 범위(index). Defaults to 100.

        Returns:
            bool: 왼쪽 커브인 경우 True, 오른쪽 커브인 경우 False
        """
        left_line = self.map_data.get_left_line()
        right_line = self.map_data.get_right_line()

        # find start point
        lstart_point_index = self.map_data.get_left_mod_index(left_index - detect_range)
        rstart_point_index = self.map_data.get_right_mod_index(right_index - detect_range)
        lstart_point:np.ndarray = left_line[lstart_point_index]
        rstart_point:np.ndarray = right_line[rstart_point_index]

        ## 내적을 통해 왼쪽 커브인지 오른쪽 커브인지 판단

        # start point에서 시작해서 detect_range안의 점들로 가는 벡터의 합을 구한다.
        # 우선 detect_range안의 점들의 합을 구한다.
        sum_left:np.ndarray = np.array([0, 0], dtype=np.float32)
        sum_right:np.ndarray = np.array([0, 0], dtype=np.float32)

        for i in range(2*detect_range-1):
            lnext_point_index = self.map_data.get_left_mod_index(left_index + i - detect_range)
            rnext_point_index = self.map_data.get_right_mod_index(right_index + i - detect_range)

            sum_left += left_line[lnext_point_index]
            sum_right += right_line[rnext_point_index]
        
        # 더한 점들의 개수만큼 start point를 곱하여 빼준다.
        sum_left_vector:np.ndarray = sum_left - lstart_point*(2*detect_range-1)
        sum_right_vector:np.ndarray = sum_right - rstart_point*(2*detect_range-1)

        # find end point
        llast_point_index = self.map_data.get_left_mod_index(left_index + detect_range)
        rlast_point_index = self.map_data.get_right_mod_index(right_index + detect_range)

        # make standard vector
        left_standard_vector:np.ndarray = left_line[llast_point_index] - lstart_point
        right_standard_vector:np.ndarray = right_line[rlast_point_index] - rstart_point

        # normalize standard vector
        left_standard_vector /= np.linalg.norm(left_standard_vector)
        right_standard_vector /= np.linalg.norm(right_standard_vector)

        rotation_matrix:np.ndarray = np.array([[0, -1], [1, 0]], dtype=np.float32)

        dot_prod:float = np.dot(rotation_matrix @ left_standard_vector, sum_left_vector)\
              + np.dot(rotation_matrix @ right_standard_vector, sum_right_vector)
        
        if dot_prod < 0:
            return True
        else:
            return False


if __name__ == "__main__":
    map_data = map.SquareMap()
    left = map_data.get_left_line()
    right = map_data.get_right_line()

    grid_node = GridNodeMap(map_data,line_dist_index=400)

    vir_line = grid_node.get_vir_line(0, 0)

    # plot
    plt.plot(left[:, 0], left[:, 1], 'r', label='left')
    plt.plot(right[:, 0], right[:, 1], 'b', label='right')
    for i in range(len(vir_line)):
        left_index = vir_line[i][0]
        right_index = vir_line[i][1]
        left_index = map_data.get_left_mod_index(left_index)
        right_index = map_data.get_right_mod_index(right_index)
        plt.plot([left[left_index][0], right[right_index][0]],[left[left_index][1], right[right_index][1]], 'g')
    plt.legend()
    plt.show()