from vertical_line_in_map import VerticalLineMap
import matplotlib.pyplot as plt 
from implement_defs.make_sqare_map import SquareMap
import numpy as np

if __name__ == "__main__":
    map_data = SquareMap()
    left = map_data.get_left_line()
    right = map_data.get_right_line()

    grid_line = VerticalLineMap(map_data,line_dist_index=400)

    ver_line_index = grid_line.get_ver_line_index(0, 0)

    ver_coord_data = grid_line.get_ver_line_coord(ver_line_index)

    ver_coord = ver_coord_data.coordinate

    # plot
    plt.plot(left[:, 0], left[:, 1], 'r', label='left')
    plt.plot(right[:, 0], right[:, 1], 'b', label='right')
    for i in range(len(ver_coord)):
        coord = np.transpose(ver_coord[i])
        plt.plot(coord[0], coord[1], 'g')
    plt.legend()
    plt.show()