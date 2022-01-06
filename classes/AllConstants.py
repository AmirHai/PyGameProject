import pygame
import sqlite3

WIDTH = 1280
HEIGHT = 720
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BUTTONSIZE = (300, 100)
HEROSIZE = (40, 40)
# точка ценра для прорисовки главного героя
CENTER = (620, 340)
STOREITEMSIZE = (120, 80)
PIXELSIZE = 40
CON = sqlite3.connect('game_info.sqlite')
CUR = CON.cursor()
