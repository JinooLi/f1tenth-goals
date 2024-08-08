import numpy as np
import matplotlib.pyplot as plt 

class map_line_data:
    def __init__(self, leftline:np, rightline:np):
        self.leftline = leftline
        self.rightline = rightline

    # 네모 맵 생성
    def __init__(self):
        right= np.array([[0, 0], [1000, 0], [1000, 1000], [0, 1000], [0, 0]], dtype=np.float32)
        left= np.array([[100, 100], [900, 100], [900, 900], [100, 900], [100, 100]], dtype=np.float32)

        self.leftline = np.array([left[0]], dtype=np.float32)
        self.rightline = np.array([right[0]], dtype=np.float32)

        for i in range(len(left)-1):
            dot_num = int(np.linalg.norm(left[i+1] - left[i]))*10
            for j in range(dot_num):
                self.leftline = np.append(self.leftline, [left[i] + (left[i+1] - left[i]) * j/dot_num], axis=0)

        for i in range(len(right)-1):
            dot_num = int(np.linalg.norm(right[i+1] - right[i]))*10
            for j in range(dot_num):
                self.rightline = np.append(self.rightline, [right[i] + (right[i+1] - right[i]) * j/dot_num], axis=0)

        self.leftline = np.delete(self.leftline, 0, axis=0)
        self.rightline = np.delete(self.rightline, 0, axis=0)

        print(self.leftline)
        print(self.rightline)

        self.left_index = len(self.leftline)
        self.right_index = len(self.rightline)
    
    def get_left_line(self)->np:
        return self.leftline
    
    def get_right_line(self)->np:
        return self.rightline

    def get_left_circuler_index(self, index:int)->int:
        return index % self.left_index
    
    def get_right_circuler_index(self, index:int)->int:
        return index % self.right_index
        

class grid_node_map:
    def __init__(self, map_data:map_line_data, line_div_num:int = 5, line_dist_index:int = 1000):
        self.map_data = map_data
        self.line_div_num = line_div_num
        self.line_dist_index = line_dist_index

    def get_grid_node(self)->np:
        grid_node = np.zeros((1, self.line_div_num), dtype=np.float32)
        pass

    def get_grid_line(self)->np:
        left_line = self.map_data.get_left_line()
        right_line = self.map_data.get_right_line()

        # 처음 수직선을 그릴 기준점을 정한다.
        # 이때, 오른쪽 커브인지 외쪽 커브인지 판단한다.
        # 오른쪽 커브인 경우, 왼쪽 점을 기준으로 수직선을 그린다. 반대는 오른쪽 점으로 한다.
        if self.is_left_curve(left_index = 0, right_index = 0):
            pass
        else:
            pass

    # index번째 점을 기준으로 detect_range만큼의 점을 이용하여 왼쪽 커브인지 오른쪽 커브인지 판단
    def is_left_curve(self, left_index:int, right_index:int, detect_range:int = 4)->bool:
        left_line = self.map_data.get_left_line()
        right_line = self.map_data.get_right_line()

        # find start point
        lstart_point_index = self.map_data.get_left_circuler_index(left_index - detect_range)
        rstart_point_index = self.map_data.get_right_circuler_index(right_index - detect_range)
        lstart_point = left_line[lstart_point_index]
        rstart_point = right_line[rstart_point_index]

        ## 내적을 통해 왼쪽 커브인지 오른쪽 커브인지 판단
        sum_left = np.array([0, 0], dtype=np.float32)
        sum_right = np.array([0, 0], dtype=np.float32)

        for i in range(2*detect_range-1):
            lnext_point_index = self.map_data.get_left_circuler_index(left_index + i - detect_range)
            rnext_point_index = self.map_data.get_right_circuler_index(right_index + i - detect_range)

            sum_left += left_line[lnext_point_index]
            sum_right += right_line[rnext_point_index]
        
        sum_left_vector = sum_left - lstart_point*(2*detect_range-1)
        sum_right_vector = sum_right - rstart_point*(2*detect_range-1)

        # find end point
        llast_point_index = self.map_data.get_left_circuler_index(left_index + detect_range)
        rlast_point_index = self.map_data.get_right_circuler_index(right_index + detect_range)

        # make standard vector
        left_standard_vector = left_line[llast_point_index] - lstart_point
        right_standard_vector = right_line[rlast_point_index] - rstart_point

        # normalize standard vector
        left_standard_vector /= np.linalg.norm(left_standard_vector)
        right_standard_vector /= np.linalg.norm(right_standard_vector)

        rotation_matrix = np.array([[0, -1], [1, 0]], dtype=np.float32)

        dot_prod = np.dot(rotation_matrix @ left_standard_vector, sum_left_vector)\
              + np.dot(rotation_matrix @ right_standard_vector, sum_right_vector)

        if dot_prod < 0:
            return True
        else:
            return False


if __name__ == "__main__":
    map_data = map_line_data()
    left = map_data.get_left_line()
    right = map_data.get_right_line()

    grid_node = grid_node_map(map_data)

    print(len(left))

    if grid_node.is_left_curve(0,0):
        print("left curve")
    else:
        print("right curve")

    # plot
    plt.plot(left[:, 0], left[:, 1], 'r', label='left')
    plt.plot(right[:, 0], right[:, 1], 'b', label='right')
    plt.legend()
    plt.show()