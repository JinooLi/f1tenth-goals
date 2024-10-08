import numpy as np
from core.definition import LineType, MapLineData, VerLineData

class VerticalLineMap:
    def __init__(self, 
                map_data:MapLineData, 
                line_div_num:int = 5, 
                line_dist_index:int = 700,
                start_x_index:int =0,
                start_y_index:int =0):
        """
        맵을 나누는 수직선들을 만드는 클래스

        Args:
            map_data (MapLineData): 맵 정보를 담은 클래스
            line_div_num (int, optional): 수직선 위의 노드 개수. Defaults to 5.
            line_dist_index (int, optional): 수직선간 최대 거리(인덱스임). Defaults to 700.
            start_x_index (int, optional): 수직선의 시작 x index. Defaults to 0.
            start_y_index (int, optional): 수직선의 시작 y index. Defaults to 0.
        """
        # init
        self.map_data = map_data
        self.left_line = map_data.get_left_line()
        self.right_line = map_data.get_right_line()
        self.line_div_num = line_div_num
        self.line_dist_index = line_dist_index

        # make vertical line
        self.ver_line_index = self.make_ver_line_index(start_x_index, start_y_index)
        self.ver_line_data = self.make_ver_line_coord(self.ver_line_index)

    def get_ver_line_data(self)->VerLineData:
        """수직선 데이터를 반환하는 함수

        Returns:
            VerLineData: 수직선들의 좌표를 담은 클래스.
            VerLineData.coordinate = [ [ [left x좌표1, left y좌표1], [right x좌표1, right y좌표1] ], [ ~2, ~2 ], ... ]
        """
        return self.ver_line_data
    
    def get_ver_line_index(self)->np.ndarray:
        """수직선의 index를 반환하는 함수

        Returns:
            ver_line_index (np.ndarray): 수직선들의 왼쪽 점과 오른쪽 점의 index를 담은 배열.
            [ [ left point index1, right point index1 ], [ ~2, ~2 ], ... ]
        """
        return self.ver_line_index

    def make_ver_line_coord(self, ver_line_index:np.ndarray)->VerLineData:
        """
        수직선들의 좌표를 반환하는 함수

        Args:
            ver_line_index (np.ndarray): 수직선들의 왼쪽 점과 오른쪽 점의 index를 담은 배열.
            [ [ left point index1, right point index1 ], [ ~2, ~2 ], ... ]

        Returns:
            VerLineData: 수직선들의 좌표를 담은 클래스.
            VerLineData.coordinate = [ [ [left x좌표1, left y좌표1], [right x좌표1, right y좌표1] ], [ ~2, ~2 ], ... ]
        """

        ver_line_coord = np.zeros((len(ver_line_index), 2, 2), dtype=np.float32)
        for i in range(len(ver_line_index)):
            left_index = ver_line_index[i][0]
            right_index = ver_line_index[i][1]

            left_abs_index = self.map_data.get_left_mod_index(left_index)
            right_abs_index = self.map_data.get_right_mod_index(right_index)

            ver_line_coord[i][0] = self.left_line[left_abs_index]
            ver_line_coord[i][1] = self.right_line[right_abs_index]

        ver_line_data = VerLineData(coordinate=ver_line_coord)
        return ver_line_data
        

    def make_ver_line_index(self, left_start_index:int, right_start_index:int)->np.ndarray:
        """
        맵을 나누는 수직선들을 만드는 함수. 각각의 수직선들은 두 개의 점으로 이루어진다.

        Args:
            left_start_index (int): 왼쪽 라인의 시작 index
            right_start_index (int): 오른쪽 라인의 시작 index

        Returns:
            ver_line_index (np.ndarray): 수직선들의 왼쪽 점과 오른쪽 점의 index를 담은 배열.
            [ [ left point index1, right point index1 ], [ ~2, ~2 ], ... ]
        """

        # 처음 수직선을 그릴 기준점을 정한다.
        # 이때, 오른쪽 커브인지 외쪽 커브인지 판단한다.
        # 오른쪽 커브인 경우, 왼쪽 점을 기준으로 수직선을 그린다. 반대는 오른쪽 점으로 한다.

        flag:LineType = LineType.UNKNOWN
        if self.is_left_curve(left_index = left_start_index, right_index = right_start_index, detect_range= self.line_dist_index):  
            right_start_abs_index = self.map_data.get_right_mod_index(right_start_index)
            right_start_point:np.ndarray = self.right_line[right_start_abs_index]

            min_norm_left_index:int = left_start_index
            abs_index = self.map_data.get_left_mod_index(min_norm_left_index)
            min_norm:float = float(np.linalg.norm(self.left_line[abs_index] - right_start_point))

            for i in range(2 * self.line_dist_index): # 왼쪽 라인의 점들 중에서 가장 가까운 점을 찾는다. 이때 앞뒤로 line_dist_index 개 안에서 찾는다.
                left_index = left_start_index - self.line_dist_index + i
                left_abs_index = self.map_data.get_left_mod_index(left_index)
                norm:float = np.linalg.norm(self.left_line[left_abs_index] - right_start_point)  # type: ignore
                if norm < min_norm:
                    min_norm = norm
                    min_norm_left_index = left_index
            
            ver_line_index = np.array([[min_norm_left_index, right_start_index]], dtype=int)
            flag = LineType.RIGHT
        else: # 위와 같은 방법으로 오른쪽 커브인 경우.
            left_start_abs_index = self.map_data.get_left_mod_index(left_start_index)
            left_start_point:np.ndarray = self.left_line[left_start_abs_index]

            min_norm_right_index:int = right_start_index
            abs_index = self.map_data.get_right_mod_index(min_norm_right_index)
            min_norm:float = np.linalg.norm(self.right_line[abs_index] - left_start_point) # type: ignore

            for i in range(2 * self.line_dist_index):
                right_index = right_start_index - self.line_dist_index + i
                right_abs_index = self.map_data.get_right_mod_index(right_index)
                norm:float = np.linalg.norm(self.right_line[right_abs_index] - left_start_point) # type: ignore
                if norm < min_norm:
                    min_norm = norm
                    min_norm_right_index = right_index
            
            ver_line_index = np.array([[left_start_index, min_norm_right_index]], dtype=int)
            flag = LineType.LEFT

        # 나머지 수직선들을 그린다.
        left_line_len:int = len(self.left_line)
        right_line_len:int = len(self.right_line)
        left_index:int = ver_line_index[0][0]
        right_index:int = ver_line_index[0][1]
        while True:
            if flag == LineType.RIGHT: # 오른쪽 라인을 기준으로 왼쪽 라인을 찾는다.
                # 다음 수직선의 오른쪽 점을 가리키는 index를 구한다.
                right_index += self.line_dist_index
                
                if right_index - ver_line_index[0][1] >= right_line_len:
                    break # 오른쪽 라인의 끝에 도달하면 종료
                
                # 가장 가까운 점을 구하기 위한 초기화
                right_abs_index = self.map_data.get_right_mod_index(right_index)
                right_point:np.ndarray = self.right_line[right_abs_index]

                left_abs_index = self.map_data.get_left_mod_index(left_index)
                min_norm:float = np.linalg.norm(right_point - self.left_line[left_abs_index]) # type: ignore
                min_norm_left_index:int = left_index

                for i in range(2*self.line_dist_index):
                    index = left_index + i
                    abs_index = self.map_data.get_left_mod_index(index)
                    norm:float = np.linalg.norm(right_point - self.left_line[abs_index]) # type: ignore

                    if norm < min_norm:
                        min_norm = norm
                        min_norm_left_index = index

                left_index = min_norm_left_index
                ver_line_index = np.append(ver_line_index, [[left_index, right_index]], axis=0)

            else:
                left_index += self.line_dist_index

                if left_index - ver_line_index[0][0] >= left_line_len:
                    break

                left_abs_index = self.map_data.get_left_mod_index(left_index)
                left_point:np.ndarray = self.left_line[left_abs_index]

                right_abs_index = self.map_data.get_right_mod_index(right_index)
                min_norm:float = np.linalg.norm(left_point - self.right_line[right_abs_index]) # type: ignore
                min_norm_right_index:int = right_index

                for i in range(2*self.line_dist_index):
                    index = right_index + i
                    abs_index = self.map_data.get_right_mod_index(index)
                    norm = np.linalg.norm(left_point - self.right_line[abs_index]) # type: ignore

                    if norm < min_norm:
                        min_norm = norm
                        min_norm_right_index = index
                
                right_index = min_norm_right_index
                ver_line_index = np.append(ver_line_index, [[left_index, right_index]], axis=0)
            
            # 다음 기준점을 판단하기 위해 만든 수직선 앞의 트랙이 어떤 커브인지 판단한다.
            if self.is_left_curve(left_index + self.line_dist_index,\
                                right_index + self.line_dist_index,\
                                int(1.1*self.line_dist_index)): 
                # 여기서 detect_range는 1.1*self.line_dist_index로 설정한다.
                # 딱 line_dist_index만큼만 설정하면 코너에서 어떤 커브인지 오판할 수 있기 때문이다.
                flag = LineType.RIGHT
            else:
                flag = LineType.LEFT

        return ver_line_index
    
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

        # find start point
        lstart_point_index = self.map_data.get_left_mod_index(left_index - detect_range)
        rstart_point_index = self.map_data.get_right_mod_index(right_index - detect_range)
        lstart_point:np.ndarray = self.left_line[lstart_point_index]
        rstart_point:np.ndarray = self.right_line[rstart_point_index]

        ## 내적을 통해 왼쪽 커브인지 오른쪽 커브인지 판단

        # start point에서 시작해서 detect_range안의 점들로 가는 벡터의 합을 구한다.
        # 우선 detect_range안의 점들의 합을 구한다.
        sum_left:np.ndarray = np.array([0, 0], dtype=np.float32)
        sum_right:np.ndarray = np.array([0, 0], dtype=np.float32)

        for i in range(2*detect_range-1):
            lnext_point_index = self.map_data.get_left_mod_index(left_index + i - detect_range)
            rnext_point_index = self.map_data.get_right_mod_index(right_index + i - detect_range)

            sum_left += self.left_line[lnext_point_index]
            sum_right += self.right_line[rnext_point_index]
        
        # 더한 점들의 개수만큼 start point를 곱하여 빼준다.
        sum_left_vector:np.ndarray = sum_left - lstart_point*(2*detect_range-1)
        sum_right_vector:np.ndarray = sum_right - rstart_point*(2*detect_range-1)

        # find end point
        llast_point_index = self.map_data.get_left_mod_index(left_index + detect_range)
        rlast_point_index = self.map_data.get_right_mod_index(right_index + detect_range)

        # make standard vector
        left_standard_vector:np.ndarray = self.left_line[llast_point_index] - lstart_point
        right_standard_vector:np.ndarray = self.right_line[rlast_point_index] - rstart_point

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