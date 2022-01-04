from AllConstants import *
from serviceFunctions import *

IMAGES = {
    'wall': load_image('Стена.png'),
    'empty': load_image('Земля.png'),
    'hero': load_image('character.png')
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
    def __init__(self):
        self.board = [[0] * 100 for _ in range(100)]
        self.MainHeroPosition = [5.0, 5.0]
        self.allWalls = pygame.sprite.Group()
        self.WallKoordinates = set()
        self.allEmpty = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        for i in range(ROOMSIZE):
            for j in range(ROOMSIZE):
                x_change = CENTER[0] - round((self.MainHeroPosition[0] - i) * PIXELSIZE)
                y_change = CENTER[1] - round((self.MainHeroPosition[1] - j) * PIXELSIZE)
                # тут позже появится обработка карты по шаблону, сами шаблоны потом будут сгенерированны
                # обработку поля я вынесу в отдельную функцию))))
                if i == 0 or i == ROOMSIZE - 1 or j == 0 or j == ROOMSIZE - 1:
                    Wall('wall', x_change, y_change, self.allWalls)
                    self.WallKoordinates.add((i, j))
                    self.WallKoordinates.add((i - 1, j))
                    self.WallKoordinates.add((i, j - 1))
                else:
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
