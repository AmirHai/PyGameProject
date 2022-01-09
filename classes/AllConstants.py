import pygame
import sqlite3

WIDTH = 1280
HEIGHT = 720
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BUTTON_SIZE = (300, 100)
HERO_SIZE = (40, 40)
# точка ценра для прорисовки главного героя
CENTER = (620, 340)
STORE_ITEM_SIZE = (120, 80)
PIXEL_SIZE = 40
CON = sqlite3.connect('game_info.sqlite')
CUR = CON.cursor()
MONSTER_VISION = 13
