from io import SEEK_CUR
import pygame
from settings import *
vec = pygame.math.Vector2
from a_star import a_star
from random import randint
import math


class Player:

    def __init__(self, app, position):
        self.current_score = 0
        self.high_score = 0
        self.app = app
        self.starting_position = [position.x, position.y]
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.direction = vec(1,0)
        self.stored_direction = None
        self.able_to_move = True
        self.speed = 1
        self.lives = 3
        self.target = None
        self.auto_play = True
        self.won = True
        self.isAngry = False
        self.counter = 0

    def update(self):

        if self.isAngry:
            if self.counter <= 0:
                self.isAngry = False
                self.speed = 1
                for enemy in self.app.enemies:
                    enemy.change_personality('ucs')
            else:
                self.counter -= 10

        if self.able_to_move:
            self.pixel_position += self.direction*self.speed

        if self.auto_play:
            self.auto_move()
        elif self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        
        self.grid_position[0] = (self.pixel_position[0] - top_bottom_buffer + self.app.cell_width//2)//self.app.cell_width+1
        self.grid_position[1] = (self.pixel_position[1] - top_bottom_buffer + self.app.cell_height//2)//self.app.cell_height+1

        if self.on_coin():
            self.eat_coin(False)

        if self.on_superCoin():
            self.eat_coin(True)

        print(len(self.app.coins))
        print(len(self.app.superCoins))

        if len(self.app.coins) == 0 and len(self.app.superCoins) == 0:
            self.endgame()

    def draw(self):
        pygame.draw.circle(self.app.screen, player_colour, (int(self.pixel_position.x), int(self.pixel_position.y)), self.app.cell_width//2-2)

        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, player_colour, (30 + 40 * x, height - 15), 10)

    def auto_move(self):
        if self.target is None:
            self.target = self.set_coin_target()
            if self.target[0] == self.grid_position[0] and self.target[1] == self.grid_position[1]:
                if self.target in self.app.coins:
                    self.eat_coin(False)
                if self.target in self.app.superCoins:
                    self.eat_coin(True)
        self.pixel_position += self.direction * self.speed
        if self.time_to_move():
            self.direction = self.get_path_direction(self.target)

    def switch_to_angry_mode(self):
        self.isAngry = True
        self.counter = 10000
        self.speed = 2
        for enemy in self.app.enemies:
            enemy.change_personality('random')

    # def minimax_move(self, matrix):
    #     # current_coord = self.get_matrix_coordinates()
    #     # if current_coord == self.target:
    #     #     self.target = None
    #     # if self.target is None:  # and self.time_counter % 50 == 0:
    #     self.set_new_target()
    #     if self.target is not None:
    #         state = GameState(matrix)
    #         enemies_coords = state.get_enemies_positions()
    #         if self.root_node is not None:
    #             nodes = [item for sublist in
    #                 list(map(lambda child: child.children, self.root_node.children))
    #              for item in sublist]
    #             big_flag = False
    #             for last_node in nodes:
    #                 last_enemies_coords = last_node.state.get_enemies_positions()
    #                 flag = True
    #                 for enemies_coord in enemies_coords:
    #                     if enemies_coord not in last_enemies_coords:
    #                         flag = False
    #                         break

    #                 if flag:
    #                     self.root_node = last_node
    #                     generate_tree_recurs(last_node, 1, self.matrix, self.target)
    #                     print('FOUND')
    #                     big_flag = True
    #                     break
    #             # if not big_flag:
    #             self.root_node = generate_tree(state, self.target)
    #         else:
    #             self.root_node = generate_tree(state, self.target)
    #         best_value = minimax(self.root_node, -math.inf, math.inf, 0)
    #         # best_value = expectimax(self.root_node, 0)

    #         pacman_position = self.get_matrix_coordinates()
    #         for child in self.root_node.children:
    #             if child.value == best_value:
    #                 new_position = child.state.get_pacman_position()
    #                 delta = (pacman_position[0] - new_position[0],
    #                          pacman_position[1] - new_position[1])
    #                 new_direction = self.vector_dict.get(delta)
    #                 if new_direction is not None:
    #                     self.direction = new_direction
    #                 else:
    #                     self.set_new_target()
    #                 break
    #     self.time_to_move()

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        if next_cell is None:
            return vec(0, 0)
        xdir = next_cell[0] - self.grid_position[0]
        ydir = next_cell[1] - self.grid_position[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = a_star(self.app.matrix,
                        [int(self.grid_position.x), int(self.grid_position.y)],
                        [int(target[0]), int(target[1])])
        if len(path) < 2:
            self.target = None
        else:
            return path[1]

    def set_coin_target(self):
        coins = self.app.coins + self.app.superCoins
        target = coins[randint(0, len(coins) - 1)]
        return target

    def on_coin(self):
        if self.grid_position in self.app.coins:
            if int(self.pixel_position.x + top_bottom_buffer//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pixel_position.y + top_bottom_buffer//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def on_superCoin(self):
        if self.grid_position in self.app.superCoins:
            if int(self.pixel_position.x + top_bottom_buffer//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pixel_position.y + top_bottom_buffer//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False


    def eat_coin(self, onSuper):
        if onSuper:
            self.app.superCoins.remove(self.grid_position)
            self.current_score += 25
            self.switch_to_angry_mode()
        else:
            self.app.coins.remove(self.grid_position)
            self.current_score += 10

    def move(self, direction):
        self.stored_direction = direction

    def get_pixel_position(self):
        return vec((self.grid_position.x*self.app.cell_width) + top_bottom_buffer//2 + self.app.cell_width//2, 
        self.grid_position.y*self.app.cell_height  + top_bottom_buffer//2 + self.app.cell_height//2)

    def get_pixel_position_from_grid(self, x, y):
        return vec(int((x * self.app.cell_width) + top_bottom_buffer // 2),
                   int((y * self.app.cell_height) + top_bottom_buffer // 2))

    def time_to_move(self):
        if int(self.pixel_position.x + top_bottom_buffer//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pixel_position.y + top_bottom_buffer//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_position + self.direction) == wall:
                return False
        return True

    def endgame(self):
        self.app.state = 'endgame'
        if self.high_score < self.current_score:
            self.high_score = self.current_score
            
