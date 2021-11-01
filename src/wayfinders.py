import time
import queue


def get_neighbors(matrix, current_coord):
    (cy, cx) = current_coord
    neighboring_nodes = [(cy-1, cx), (cy, cx+1), (cy+1, cx), (cy, cx-1)]

    neighboring_nodes = list(filter(
        lambda node: matrix[node[0]][node[1]] != 1 and node[0] >= 0 and node[0] < len(
            matrix) and node[1] >= 0 and node[1] < len(matrix[0]),
        neighboring_nodes
    ))

    return neighboring_nodes