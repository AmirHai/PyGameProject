import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_map(name):
    board = []
    file = open(f'./maps/{name}.csv', encoding='utf8').read()
    file = file.split('\n')
    for i in file:
        board.append([int(j) for j in i.split(' ')])
    return board
