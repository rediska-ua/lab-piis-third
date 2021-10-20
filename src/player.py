from io import SEEK_CUR
import pygame
from settings import *
vec = pygame.math.Vector2
from a_star import a_star
from random import randint

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

    def update(self):
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
            self.eat_coin()

        if len(self.app.coins) == 0:
            self.endgame()

    def draw(self):
        pygame.draw.circle(self.app.screen, player_colour, (int(self.pixel_position.x), int(self.pixel_position.y)), self.app.cell_width//2-2)

        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, player_colour, (30 + 40 * x, height - 15), 10)

    def auto_move(self):
        if self.target is None:
            self.target = self.set_coin_target()
        print(self.target)
        self.pixel_position += self.direction * self.speed
        if self.time_to_move():
            self.direction = self.get_path_direction(self.target)

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
        target = self.app.coins[randint(0, len(self.app.coins) - 1)]
        pix_pos = self.get_pixel_position_from_grid(target[0], target[1])
        print(pix_pos)
        pygame.draw.rect(self.app.screen, green,
                             (pix_pos[0], pix_pos[1], self.app.cell_width, self.app.cell_height))
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

    def eat_coin(self):
        self.app.coins.remove(self.grid_position)
        self.current_score += 1

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
            
