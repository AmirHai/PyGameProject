import pygame.sprite

from AllConstants import *
from serviceFunctions import *

IMAGES = {
    'wall': load_image('Стена.png'),
    'empty': load_image('Земля.png'),
    'hero': load_image('./characterGif/перс-аним1.png')
}


# тут находятся мелкие подклассы клеток стены и пола, которые будут задаваться для поля.
# тут я разместил их специально, так как будет намного легче за ними следить в основном классе
class Wall(pygame.sprite.Sprite):
    def __init__(self, walls_type, pos_x, pos_y, group):
        super().__init__(group)
        self.image = pygame.transform.scale(IMAGES[walls_type], (40, 40))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.image = pygame.transform.scale(IMAGES[player], (PIXEL_SIZE, PIXEL_SIZE))
        self.rect = self.image.get_rect().move(CENTER[0], CENTER[1])


class Weapon(pygame.sprite.Sprite):
    def __init__(self, group, name):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(name + '.png'), (PIXEL_SIZE * 0.75, PIXEL_SIZE * 0.5))
        self.rect = self.image.get_rect().move(CENTER[0] + PIXEL_SIZE * 0.75, CENTER[1] + PIXEL_SIZE * 0.5)


class Camera:
    def __init__(self):
        self.xChan = 0
        self.yChan = 0

    def apply(self, obj):
        for i in obj:
            i.rect.x += self.xChan
            i.rect.y += self.yChan

    def update(self, x, y):
        self.xChan = x
        self.yChan = y


# основной класс карты игры, в котором происходит обработка поля во время ходьбы
class GameMap:
    def __init__(self, level):
        self.board = [[0] * 115 for _ in range(115)]
        self.MainHeroPosition = [5.0, 5.0]
        self.allWalls = pygame.sprite.Group()
        self.wall_coordinates = set()
        self.empty_coordinates = []
        self.allEmpty = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        self.map_handler(level)
        Player('hero', self.playerGroup)
        self.PlayerLife = 6

    def map_handler(self, level):
        self.board = load_map(f'{str(level)}levelMap')
        for i in range(25):
            self.empty_coordinates.append([])
        for i in range(115):
            for j in range(115):
                if self.board[i][j] == 4:
                    self.MainHeroPosition = [float(i), float(j)]
        for i in range(115):
            for j in range(115):
                x_change = CENTER[0] - round((self.MainHeroPosition[0] - i) * PIXEL_SIZE)
                y_change = CENTER[1] - round((self.MainHeroPosition[1] - j) * PIXEL_SIZE)
                if self.board[i][j] == 2:
                    Wall('wall', x_change, y_change, self.allWalls)
                    self.wall_coordinates.add((i, j))
                    self.wall_coordinates.add((i - 1, j))
                    self.wall_coordinates.add((i, j - 1))
                elif self.board[i][j] == 1:
                    self.empty_coordinates[(i // 25) * 5 + j // 25].append([i, j])
                    Wall('empty', x_change, y_change, self.allEmpty)
                elif self.board[i][j] == 3 or self.board[i][j] == 4:
                    Wall('empty', x_change, y_change, self.allEmpty)
        Player('hero', self.playerGroup)

    def render(self):
        SCREEN.fill('Black')
        self.allWalls.draw(SCREEN)
        self.allEmpty.draw(SCREEN)
        self.playerGroup.draw(SCREEN)

    def wall_helper(self, moving):
        changed_move = moving
        if (int(self.MainHeroPosition[0] - moving[0]), int(self.MainHeroPosition[1])) in self.wall_coordinates:
            changed_move[0] = 0.0
        if (int(self.MainHeroPosition[0]), int(self.MainHeroPosition[1] - moving[1])) in self.wall_coordinates:
            changed_move[1] = 0.0
        return changed_move
