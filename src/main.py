from vertical_line_in_map import VerticalLineMap
import matplotlib.pyplot as plt 
from implement_defs.make_sqare_map import SquareMap

if __name__ == "__main__":
    map_data = SquareMap()
    left = map_data.get_left_line()
    right = map_data.get_right_line()

    grid_node = VerticalLineMap(map_data,line_dist_index=400)

    vir_line = grid_node.get_vir_line_index(0, 0)

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