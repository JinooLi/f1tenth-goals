import numpy as np
import matplotlib.pyplot as plt 
from core.definition import LineType

class MapLineData:
    def __init__(self, leftline:np, rightline:np):
        self.leftline = leftline
        self.rightline = rightline

    # 네모 맵 생성
    def __init__(self):
        right= np.array([[0, 0], [1000, 0], [1000, 1000], [0, 1000], [0, 0]], dtype=np.float32)
        left= np.array([[100, 100], [900, 100], [900, 900], [100, 900], [100, 100]], dtype=np.float32)

        # append하기 위한 초기화
        self.leftline = np.array([left[0]], dtype=np.float32)
        self.rightline = np.array([right[0]], dtype=np.float32)

        # 점 두 개 사이에 점 사이의 거리 x 10만큼의 점을 찍는다.
        for i in range(len(left)-1):
            dot_num = int(np.linalg.norm(left[i+1] - left[i]))*10
            for j in range(dot_num):
                self.leftline = np.append(self.leftline, [left[i] + (left[i+1] - left[i]) * j/dot_num], axis=0)

        for i in range(len(right)-1):
            dot_num = int(np.linalg.norm(right[i+1] - right[i]))*10
            for j in range(dot_num):
                self.rightline = np.append(self.rightline, [right[i] + (right[i+1] - right[i]) * j/dot_num], axis=0)

        # 초기화를 위한 첫번째 점 제거
        self.leftline = np.delete(self.leftline, 0, axis=0)
        self.rightline = np.delete(self.rightline, 0, axis=0)

        # print(self.leftline)
        # print(self.rightline)

        self.left_index = len(self.leftline)
        self.right_index = len(self.rightline)
    
    def get_left_line(self)->np.ndarray:
        return self.leftline
    
    def get_right_line(self)->np.ndarray:
        return self.rightline

    def get_left_circuler_index(self, index:int)->int:
        return index % self.left_index
    
    def get_right_circuler_index(self, index:int)->int:
        return index % self.right_index
        

class GridNodeMap:
    def __init__(self, map_data:MapLineData, line_div_num:int = 5, line_dist_index:int = 700):
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

    def get_grid_node(self)->np.ndarray:
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
        left_line = self.map_data.get_left_line()
        right_line = self.map_data.get_right_line()

        # 처음 수직선을 그릴 기준점을 정한다.
        # 이때, 오른쪽 커브인지 외쪽 커브인지 판단한다.
        # 오른쪽 커브인 경우, 왼쪽 점을 기준으로 수직선을 그린다. 반대는 오른쪽 점으로 한다.

        flag:LineType = LineType.UNKNOWN
        if self.is_left_curve(left_index = left_start_index, right_index = right_start_index, detect_range= self.line_dist_index):  
            right_start_abs_index = self.map_data.get_right_circuler_index(right_start_index)
            right_start_point:np = right_line[right_start_abs_index]

            min_norm_left_index:int = left_start_index
            abs_index = self.map_data.get_left_circuler_index(min_norm_left_index)
            min_norm:float = np.linalg.norm(left_line[abs_index] - right_start_point)

            for i in range(2 * self.line_dist_index): # 왼쪽 라인의 점들 중에서 가장 가까운 점을 찾는다. 이때 앞뒤로 line_dist_index 개 안에서 찾는다.
                left_index = left_start_index - self.line_dist_index + i
                left_abs_index = self.map_data.get_left_circuler_index(left_index)
                norm = np.linalg.norm(left_line[left_abs_index] - right_start_point)
                if norm < min_norm:
                    min_norm = norm
                    min_norm_left_index = left_index
            
            vir_line_index = np.array([[min_norm_left_index, right_start_index]], dtype=int)
            flag = LineType.RIGHT
        else: # 위와 같은 방법으로 오른쪽 커브인 경우.
            left_start_abs_index = self.map_data.get_left_circuler_index(left_start_index)
            left_start_point:np = left_line[left_start_abs_index]

            min_norm_right_index:int = right_start_index
            abs_index = self.map_data.get_right_circuler_index(min_norm_right_index)
            min_norm:float = np.linalg.norm(right_line[abs_index] - left_start_point)

            for i in range(2 * self.line_dist_index):
                right_index = right_start_index - self.line_dist_index + i
                right_abs_index = self.map_data.get_right_circuler_index(right_index)
                norm = np.linalg.norm(right_line[right_abs_index] - left_start_point)
                if norm < min_norm:
                    min_norm = norm
                    min_norm_right_index = right_index
            
            vir_line_index = np.array([[left_start_index, min_norm_right_index]], dtype=int)
            flag = LineType.LEFT

        # 나머지 수직선들을 그린다.
        left_line_len:int = len(left_line)
        right_line_len:int = len(right_line)
        left_index:int = vir_line_index[0][0]
        right_index:int = vir_line_index[0][1]
        while True:
            if flag == LineType.RIGHT: # 오른쪽 라인을 기준으로 왼쪽 라인을 찾는다.
                # 다음 수직선의 오른쪽 점을 가리키는 index를 구한다.
                right_index += self.line_dist_index
                
                if right_index - vir_line_index[0][1] >= right_line_len:
                    break # 오른쪽 라인의 끝에 도달하면 종료
                
                # 가장 가까운 점을 구하기 위한 초기화
                right_abs_index = self.map_data.get_right_circuler_index(right_index)
                right_point:np = right_line[right_abs_index]

                left_abs_index = self.map_data.get_left_circuler_index(left_index)
                min_norm:float = np.linalg.norm(right_point - left_line[left_abs_index])
                min_norm_left_index:int = left_index

                for i in range(2*self.line_dist_index):
                    index = left_index + i
                    abs_index = self.map_data.get_left_circuler_index(index)
                    norm = np.linalg.norm(right_point - left_line[abs_index])

                    if norm < min_norm:
                        min_norm = norm
                        min_norm_left_index = index

                left_index = min_norm_left_index
                vir_line_index = np.append(vir_line_index, [[left_index, right_index]], axis=0)

            else:
                left_index += self.line_dist_index

                if left_index - vir_line_index[0][0] >= left_line_len:
                    break

                left_abs_index = self.map_data.get_left_circuler_index(left_index)
                left_point:np = left_line[left_abs_index]

                right_abs_index = self.map_data.get_right_circuler_index(right_index)
                min_norm:float = np.linalg.norm(left_point - right_line[right_abs_index])
                min_norm_right_index:int = right_index

                for i in range(2*self.line_dist_index):
                    index = right_index + i
                    abs_index = self.map_data.get_right_circuler_index(index)
                    norm = np.linalg.norm(left_point - right_line[abs_index])

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
        lstart_point_index = self.map_data.get_left_circuler_index(left_index - detect_range)
        rstart_point_index = self.map_data.get_right_circuler_index(right_index - detect_range)
        lstart_point:np = left_line[lstart_point_index]
        rstart_point:np = right_line[rstart_point_index]

        ## 내적을 통해 왼쪽 커브인지 오른쪽 커브인지 판단

        # start point에서 시작해서 detect_range안의 점들로 가는 벡터의 합을 구한다.
        # 우선 detect_range안의 점들의 합을 구한다.
        sum_left:np = np.array([0, 0], dtype=np.float32)
        sum_right:np = np.array([0, 0], dtype=np.float32)

        for i in range(2*detect_range-1):
            lnext_point_index = self.map_data.get_left_circuler_index(left_index + i - detect_range)
            rnext_point_index = self.map_data.get_right_circuler_index(right_index + i - detect_range)

            sum_left += left_line[lnext_point_index]
            sum_right += right_line[rnext_point_index]
        
        # 더한 점들의 개수만큼 start point를 곱하여 빼준다.
        sum_left_vector:np = sum_left - lstart_point*(2*detect_range-1)
        sum_right_vector:np = sum_right - rstart_point*(2*detect_range-1)

        # find end point
        llast_point_index = self.map_data.get_left_circuler_index(left_index + detect_range)
        rlast_point_index = self.map_data.get_right_circuler_index(right_index + detect_range)

        # make standard vector
        left_standard_vector:np = left_line[llast_point_index] - lstart_point
        right_standard_vector:np = right_line[rlast_point_index] - rstart_point

        # normalize standard vector
        left_standard_vector /= np.linalg.norm(left_standard_vector)
        right_standard_vector /= np.linalg.norm(right_standard_vector)

        rotation_matrix:np = np.array([[0, -1], [1, 0]], dtype=np.float32)

        dot_prod:float = np.dot(rotation_matrix @ left_standard_vector, sum_left_vector)\
              + np.dot(rotation_matrix @ right_standard_vector, sum_right_vector)
        
        if dot_prod < 0:
            return True
        else:
            return False


if __name__ == "__main__":
    map_data = MapLineData()
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
        left_index = map_data.get_left_circuler_index(left_index)
        right_index = map_data.get_right_circuler_index(right_index)
        plt.plot([left[left_index][0], right[right_index][0]],[left[left_index][1], right[right_index][1]], 'g')
    plt.legend()
    plt.show()