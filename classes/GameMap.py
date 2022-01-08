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
    def __init__(self, walls_type, posX, posY, Group):
        super().__init__(Group)
        self.image = pygame.transform.scale(IMAGES[walls_type], (40, 40))
        self.rect = self.image.get_rect().move(posX, posY)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, player, Group):
        super().__init__(Group)
        self.image = pygame.transform.scale(IMAGES[player], (PIXELSIZE, PIXELSIZE))
        self.rect = self.image.get_rect().move(CENTER[0], CENTER[1])


class Weapon(pygame.sprite.Sprite):
    def __init__(self, group, name):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(name + '.png'), (PIXELSIZE * 0.75, PIXELSIZE * 0.5))
        self.rect = self.image.get_rect().move(CENTER[0] + PIXELSIZE * 0.75, CENTER[1] + PIXELSIZE * 0.5)


class Camera:
    def __init__(self):
        self.xChan = 0
        self.yChan = 0

    def apply(self, obj):
        for i in obj:
            i.rect.x += self.xChan
            i.rect.y += self.yChan

    def update(self, X, Y):
        self.xChan = X
        self.yChan = Y


# основной класс карты игры, в котором происходит обработка поля во время ходьбы
class GameMap:
    def __init__(self, level):
        self.board = [[0] * 100 for _ in range(100)]
        self.MainHeroPosition = [5.0, 5.0]
        self.allWalls = pygame.sprite.Group()
        self.WallKoordinates = set()
        self.emptyKoordinates = []
        self.allEmpty = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        self.MapHandler(level)
        Player('hero', self.playerGroup)
        self.PlayerLife = 6

    def MapHandler(self, level):
        self.board = load_map(f'{str(level)}levelMap')
        for i in range(100):
            for j in range(100):
                x_change = CENTER[0] - round((self.MainHeroPosition[0] - i) * PIXELSIZE)
                y_change = CENTER[1] - round((self.MainHeroPosition[1] - j) * PIXELSIZE)
                if self.board[i][j] == 2:
                    Wall('wall', x_change, y_change, self.allWalls)
                    self.WallKoordinates.add((i, j))
                    self.WallKoordinates.add((i - 1, j))
                    self.WallKoordinates.add((i, j - 1))
                elif self.board[i][j] == 1:
                    self.emptyKoordinates.append([i, j])
                    Wall('empty', x_change, y_change, self.allEmpty)
                elif self.board[i][j] == 3:
                    Wall('empty', x_change, y_change, self.allEmpty)
        Player('hero', self.playerGroup)

    def render(self):
        SCREEN.fill('Black')
        self.allWalls.draw(SCREEN)
        self.allEmpty.draw(SCREEN)
        self.playerGroup.draw(SCREEN)

    def WallHelper(self, moving):
        ChangedMove = moving
        if (int(self.MainHeroPosition[0] - moving[0]), int(self.MainHeroPosition[1])) in self.WallKoordinates:
            ChangedMove[0] = 0.0
        if (int(self.MainHeroPosition[0]), int(self.MainHeroPosition[1] - moving[1])) in self.WallKoordinates:
            ChangedMove[1] = 0.0
        return ChangedMove
