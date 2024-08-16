import numpy as np
from core.definition import MapLineData

class SquareMap(MapLineData):
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

        # 각 라인 인덱스 개수를 저장
        self.left_index = len(self.leftline)
        self.right_index = len(self.rightline)
    
    def get_left_line(self)->np.ndarray:
        return self.leftline
    
    def get_right_line(self)->np.ndarray:
        return self.rightline

    def get_left_mod_index(self, index:int)->int:
        return index % self.left_index
    
    def get_right_mod_index(self, index:int)->int:
        return index % self.right_index