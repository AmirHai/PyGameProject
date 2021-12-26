import pygame
from AllConstants import *


class GameMap:
    def __init__(self):
        self.board = [[0] * 100 for _ in range(100)]