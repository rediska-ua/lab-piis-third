from os import pathsep
import queue
import pygame, random
import time
from settings import *
from queue import Queue, PriorityQueue

vec = pygame.math.Vector2
frontier = Queue()

class Enemy:
    def __init__(self, app, position, index):
        self.app = app
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.starting_position = [position.x, position.y]
        self.radius = 10
        self.number = index
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = 'default'
        self.best_route = None

    def get_pixel_position(self):
        return vec((self.grid_position.x*self.app.cell_width) + top_bottom_buffer//2 + self.app.cell_width//2, 
        self.grid_position.y*self.app.cell_height + top_bottom_buffer//2 + self.app.cell_height//2)

    def update(self):
        self.pixel_position += self.direction
        if self.time_to_move():
            self.move()

        self.grid_position[0] = (self.pixel_position[0] - top_bottom_buffer + self.app.cell_width//2)//self.app.cell_width+1
        self.grid_position[1] = (self.pixel_position[1] - top_bottom_buffer + self.app.cell_height//2)//self.app.cell_height+1

    def time_to_move(self):
        if int(self.pixel_position.x + top_bottom_buffer//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pixel_position.y + top_bottom_buffer//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

        return False

    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_direction()
        elif self.personality == 'default':
            self.direction = vec(0, 0)
        else:
            self.direction = self.get_path_direction()


    def get_path_direction(self):
        next_cell = self.find_next_cell_in_path()
        xdir = next_cell[0] - self.grid_position[0]
        ydir = next_cell[1] - self.grid_position[1]
        return vec(xdir, ydir)

    
    def find_next_cell_in_path(self):
        path = None
        if self.personality == 'bfs':
            path = self.BFS([int(self.grid_position.x), int(self.grid_position.y)], [int(self.app.player.grid_position.x), 
                int(self.app.player.grid_position.y)])
        elif self.personality == 'dfs':
            path = self.DFS([int(self.grid_position.x), int(self.grid_position.y)], [int(self.app.player.grid_position.x), 
                int(self.app.player.grid_position.y)])
        elif self.personality == 'ucs':
            path = self.UCS([int(self.grid_position.x), int(self.grid_position.y)], [int(self.app.player.grid_position.x), 
                int(self.app.player.grid_position.y)])

        return path[1]


    def get_neighbours(self, node):

        neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        neighbour_nodes = list(filter(
            lambda current: (node[0] + current[0] >= 0 and node[0] + current[0] < len(self.app.grid[0])) and
            (node[1] + current[1] >= 0 and node[1] + current[1] < len(self.app.grid)), neighbours
        ))

        return neighbour_nodes



    def BFS(self, start, target):
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                self.app.grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = self.get_neighbours(current)
                for neighbour in neighbours:
                    next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                    if next_cell not in visited:
                        if self.app.grid[int(next_cell[1])][int(next_cell[0])] != 1:
                            queue.append(next_cell)
                            path.append({"Current": current, "Next": next_cell})

        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest


    def DFS(self, start_node, target):

        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                self.app.grid[int(cell.y)][int(cell.x)] = 1
        stack = [start_node]
        visited = []
        path = []

        while stack:
            current = stack.pop()
            visited.append(current)

            if current == target:
                break
            
            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                next_cell = [int(neighbour[0] + current[0]), int(neighbour[1] + current[1])]
                if next_cell not in visited:
                    if self.app.grid[int(next_cell[1])][int(next_cell[0])] != 1:
                        stack.append(next_cell)
                        path.append({"Current": current, "Next": next_cell})


        route = [target]
        while target != start_node:
            for step in path:
                 if step["Next"] == target:
                    target = step["Current"]
                    route.insert(0, step["Current"])

        return route

    def UCS(self, start, target):

        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                self.app.grid[int(cell.y)][int(cell.x)] = 1

        queue = PriorityQueue()
        queue.put((0, start))
        visited = []
        path = []

        while not queue.empty():
            cost, current = queue.get()
            visited.append(current)
            if current == target:
                break
            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                if next_cell not in visited:
                    if self.app.grid[int(next_cell[1])][int(next_cell[0])] != 1:
                        queue.put((cost + 1, next_cell))
                        path.append({"Current": current, "Next": next_cell})

        route = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    route.insert(0, step["Current"])

        return route




    def get_random_direction(self):
        while True:
            number = random.randint(-2, 2)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = vec(self.grid_position.x + x_dir, self.grid_position.y + y_dir)
            if next_pos not in self.app.walls:
                break

        return vec(x_dir, y_dir)

    
    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pixel_position.x), int(self.pixel_position.y)), self.radius)

    def set_colour(self):
        if self.number == 0:
            return white
        elif self.number == 1:
            return red
        elif self.number == 2:
            return blue
        elif self.number == 3:
            return grey

    def change_personality(self, personality):
        self.personality = personality