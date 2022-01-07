from serviceFunctions import *
from AllConstants import *

TYPES = {
    'swordsman': load_image('enemy.png')
}


def IntoSpeed(numb):
    if numb > 0:
        return 0.05
    elif numb < 0:
        return -0.05
    else:
        return 0


class Monster(pygame.sprite.Sprite):
    def __init__(self, monsterType, position, playerPos, SpriteGroup, life):
        super().__init__(SpriteGroup)
        self.image = pygame.transform.scale(TYPES[monsterType], (25, 40))

        xpos = CENTER[0] - (playerPos[0] - position[0]) * PIXELSIZE
        ypos = CENTER[1] - (playerPos[1] - position[1]) * PIXELSIZE

        self.rect = self.image.get_rect().move(xpos, ypos)
        self.position = position
        self.life = life

    def moveToPlayer(self, PlayerPosition):
        if abs(PlayerPosition[0] - self.position[0]) < 10 and abs(PlayerPosition[1] - self.position[1]) < 10:
            self.speed = [IntoSpeed(PlayerPosition[0] - self.position[0]),
                          IntoSpeed(PlayerPosition[1] - self.position[1])]
        else:
            self.speed = [0.0, 0.0]

    def WallHelper(self, WallsKord):
        if (int(self.position[0] + self.speed[0]), int(self.position[1])) in WallsKord:
            self.speed[0] = 0.0
        if (int(self.position[0]), int(self.position[1] + self.speed[1])) in WallsKord:
            self.speed[1] = 0.0

    def update(self):
        self.position = [round(self.position[0] + self.speed[0], 3),
                         round(self.position[1] + self.speed[1], 3)]
        self.rect = self.rect.move(self.speed[0] * PIXELSIZE, self.speed[1] * PIXELSIZE)
