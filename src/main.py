import numpy as np
import matplotlib.pyplot as plt 
from core.vertical_line_in_map import VerticalLineMap
from implement_defs.make_sqare_map import SquareMap
from implement_defs.make_point_mass_node import PointMassNode

if __name__ == "__main__":
    # 맵 데이터 생성
    map_data = SquareMap()
    left = map_data.get_left_line()
    right = map_data.get_right_line()

    # 수직선 생성
    ver_coord_data = VerticalLineMap(map_data, line_dist_index=400).get_ver_line_data()

    # 노드 생성
    node_data = PointMassNode(ver_coord_data, maximum_speed=5.0)

    node = node_data.get_node()

    print(node[3])

    # plot
    plt.plot(left[:, 0], left[:, 1], 'r', label='left')
    plt.plot(right[:, 0], right[:, 1], 'b', label='right')
    ver_coord = ver_coord_data.coordinate
    for i in range(len(ver_coord)):
        coord = np.transpose(ver_coord[i])
        plt.plot(coord[0], coord[1], 'g')
        for j in range(node_data.node_pos_num_per_ver_line):
            index = node_data.get_node_index_on_a_line(j, 1, 0)
            plt.scatter(node[i][index][0], node[i][index][1], c='black')
    plt.legend()
    plt.show()