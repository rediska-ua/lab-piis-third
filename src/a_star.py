from copy import deepcopy
from math import e, sqrt



def get_neighbours(grid, node):
    (coord_x, coord_y) = node
    neighbour_nodes = [(coord_x + 1, coord_y), (coord_x, coord_y + 1), (coord_x - 1, coord_y), (coord_x, coord_y - 1)]

    index = 0
    while index != len(neighbour_nodes):
        (x, y) = neighbour_nodes[index]
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
            neighbour_nodes.pop(index)
        else:
            index += 1

    neighbour_nodes = list(filter(
        lambda node: grid[node[1]][node[0]] != 1 and node[1] >= 0 and node[1] < len(
            grid) and node[0] >= 0 and node[0] < len(grid[0]),
        neighbour_nodes
    ))

    return neighbour_nodes

class Node:
    def __init__(self, coord, parent_node=None):
        self.coord = coord
        self.parent_node = parent_node
        self.g = 0
        self.h = 0
        self.f = 0


def euclidean_distance(start_coord, finish_coord):
    return sqrt((start_coord[0]-finish_coord[0])**2) + ((start_coord[1]-finish_coord[1])**2)


def get_path(finish_node):
    path = []
    current = finish_node
    while current is not None:
        path.append(current.coord)
        current = current.parent_node

    path.reverse()
    return path


def a_star(matrix, start_coord, finish_coord):
    start_node = Node(start_coord)
    visited = []
    to_visit = []
    to_visit.append(start_node)
    counter = len(matrix)*len(matrix[0])

    while len(to_visit) != 0 and counter >= 0:
        counter -= 1
        curr_node = to_visit[0]
        curr_index = 0
        for i in range(len(to_visit)):
            if to_visit[i].f < curr_node.f:
                curr_node = to_visit[i]
                curr_index = i

        to_visit.pop(curr_index)
        visited.append(curr_node)

        if curr_node.coord[0] == finish_coord[0] and curr_node.coord[1] == finish_coord[1]:
            return get_path(curr_node)


        neighboring_nodes = list(map(lambda coord: Node(coord, curr_node),
                                     get_neighbours(matrix, curr_node.coord)))

        for neighbor in neighboring_nodes:

            if len([
                visited_neighbor
                for visited_neighbor in visited
                if visited_neighbor.coord[0] == neighbor.coord[0] and visited_neighbor.coord[1] == neighbor.coord[1]
            ]) > 0:
                continue

            neighbor.g = curr_node.g + 1
            neighbor.h = euclidean_distance(neighbor.coord, finish_coord)
            neighbor.f = neighbor.g + neighbor.h

            if len([
                    to_visit_node
                    for to_visit_node in to_visit
                    if to_visit_node.coord[0] == neighbor.coord[0] and to_visit_node.coord[1] == neighbor.coord[1] 
                    and to_visit_node.g < neighbor.g]) > 0:
                continue

            to_visit.append(neighbor)

    return []



