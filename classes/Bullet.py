from AllConstants import *
from serviceFunctions import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, pos, weapon_name):
        super().__init__(group)
        result = CUR.execute("""SELECT * FROM weapon_info
                    WHERE name = ?""", (weapon_name,)).fetchall()
        self.length = (pos[0] - CENTER[0] - PIXELSIZE, pos[1] - CENTER[1] - PIXELSIZE * 0.75)
        self.image = pygame.transform.scale(load_image('bullet.png'), (result[0][2], result[0][2]))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(CENTER[0] + PIXELSIZE, CENTER[1] + PIXELSIZE * 0.5)
        self.speed = result[0][1]
        self.xspeed = None
        self.yspeed = None
        if abs(self.length[0]) > abs(self.length[1]):
            time = self.length[0] / self.speed
            self.yspeed = self.length[1] / time if self.length[0] > 0 else -(self.length[1] / time)
            self.floatspeed = self.yspeed % 1 if self.yspeed > 0 else -(abs(self.yspeed) % 1)
        elif abs(self.length[0]) < abs(self.length[1]):
            time = self.length[1] / self.speed
            self.xspeed = self.length[0] / time if self.length[1] > 0 else -(self.length[0] / time)
            self.floatspeed = self.xspeed % 1 if self.xspeed > 0 else -(abs(self.xspeed) % 1)

    def update(self):
        if self.yspeed:
            self.floatspeed += self.yspeed % 1 if self.yspeed > 0 else -(abs(self.yspeed) % 1)
            self.rect = self.rect.move(self.speed if self.length[0] > 0 else -self.speed, self.yspeed)
            self.rect = self.rect.move(0, self.floatspeed)
            if abs(self.floatspeed) >= 1:
                self.floatspeed = self.floatspeed % 1 if self.yspeed > 0 else -(abs(self.floatspeed) % 1)
        elif self.xspeed:
            self.floatspeed += self.xspeed % 1 if self.xspeed > 0 else -(abs(self.xspeed) % 1)
            self.rect = self.rect.move(self.xspeed, self.speed if self.length[1] > 0 else -self.speed)
            self.rect = self.rect.move(self.floatspeed, 0)
            if abs(self.floatspeed) >= 1:
                self.floatspeed = self.floatspeed % 1 if self.xspeed > 0 else -(abs(self.floatspeed) % 1)
        else:
            self.rect = self.rect.move(self.speed if self.length[0] > 0 else -self.speed,
                                       self.speed if self.length[1] > 0 else -self.speed)
