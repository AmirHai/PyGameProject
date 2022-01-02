from AllConstants import *
from serviceFunctions import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.lenght = (pos[0] - CENTER[0] - PIXELSIZE * 0.5, pos[1] - CENTER[1] - PIXELSIZE * 0.5)
        self.image = pygame.transform.scale(load_image('bullet.png'), BULLETSIZE)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(CENTER[0] + PIXELSIZE * 0.25, CENTER[1] + PIXELSIZE * 0.25)
        self.speed = 5
        self.xspeed = None
        self.yspeed = None
        if abs(self.lenght[0]) > abs(self.lenght[1]):
            time = self.lenght[0] / self.speed
            self.yspeed = self.lenght[1] / time if self.lenght[0] > 0 else -(self.lenght[1] / time)
            self.floatspeed = self.yspeed % 1 if self.yspeed > 0 else -(abs(self.yspeed) % 1)
        elif abs(self.lenght[0]) < abs(self.lenght[1]):
            time = self.lenght[1] / self.speed
            self.xspeed = self.lenght[0] / time if self.lenght[1] > 0 else -(self.lenght[0] / time)
            self.floatspeed = self.xspeed % 1 if self.xspeed > 0 else -(abs(self.xspeed) % 1)

    def update(self):
        if self.yspeed:
            self.floatspeed += self.yspeed % 1 if self.yspeed > 0 else -(abs(self.yspeed) % 1)
            self.rect = self.rect.move(self.speed if self.lenght[0] > 0 else -self.speed, self.yspeed)
            self.rect = self.rect.move(0, self.floatspeed)
            if abs(self.floatspeed) >= 1:
                self.floatspeed = self.floatspeed % 1 if self.yspeed > 0 else -(abs(self.floatspeed) % 1)
        elif self.xspeed:
            self.floatspeed += self.xspeed % 1 if self.xspeed > 0 else -(abs(self.xspeed) % 1)
            self.rect = self.rect.move(self.xspeed, self.speed if self.lenght[1] > 0 else -self.speed)
            self.rect = self.rect.move(self.floatspeed, 0)
            if abs(self.floatspeed) >= 1:
                self.floatspeed = self.floatspeed % 1 if self.xspeed > 0 else -(abs(self.floatspeed) % 1)
        else:
            self.rect = self.rect.move(self.speed if self.lenght[0] > 0 else -self.speed,
                                       self.speed if self.lenght[1] > 0 else -self.speed)
