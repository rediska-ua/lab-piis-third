import pygame
import math
from random import randint
pygame.init()
vec = pygame.math.Vector2

ghosts = []
g_pos = []
walls = []
coins = []
p_pos = None

      
def generate_randomly():
    game_map = [[0 for x in range(28)] for x in range(30)]
    isGhostPlaced = False
    isPlayerPlaced = False
    for y in range(30):
        for x in range(28):
            if x == 0 or x == 27 or y == 0 or y == 29:
                if x == 27:
                    print(y)
                game_map[y][x] = '1'
                walls.append(vec(x, y))
            elif not isGhostPlaced:
                x1, y1 = randint(0, 27), randint(0, 29)
                while game_map[y1][x1] != 0:
                    x1, y1 = randint(0, 27), randint(0, 29)
                game_map[y1][x1] = '2'
                g_pos.append([x1, y1])
                isGhostPlaced = True
            elif not isPlayerPlaced:
                x1, y1 = randint(0, 27), randint(0, 29)
                while game_map[y1][x1] != 0:
                    x1, y1 = randint(0, 27), randint(0, 29)
                game_map[y1][x1] = 'P'
                p_pos = [x1, y1]
                isPlayerPlaced = True
            else:
                chance = randint(1, 4)
                if chance == 1:
                    game_map[y][x] = '1'
                    walls.append(vec(x, y))

    for y in range(30):
        for x in range(28):
            if game_map[y][x] == 0:
                game_map[y][x] = 'C'
                coins.append(vec(x, y))

    print(g_pos)

    save_map_to_file(game_map)

def save_map_to_file(game_map):
    with open('../assets/random_map.txt', 'w') as file:
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                file.write(game_map[y][x])
            file.write('\n')

generate_randomly()