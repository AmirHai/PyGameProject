from AllConstants import *
from serviceFunctions import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, pos, weapon_name):
        super().__init__(group)
        result = CUR.execute("""SELECT * FROM weapon_info
                    WHERE name = ?""", (weapon_name,)).fetchall()
        self.length = [pos[0] - CENTER[0] - PIXEL_SIZE, pos[1] - CENTER[1] - PIXEL_SIZE * 0.75]
        if self.length[0] == 0:
            self.length[0] = 1
        elif self.length[1] == 0:
            self.length[1] = 1
        self.image = pygame.transform.scale(load_image('bullet.png'), (result[0][2], result[0][2]))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(CENTER[0] + PIXEL_SIZE * 1.25, CENTER[1] + PIXEL_SIZE * 0.5)
        self.speed = result[0][1]
        self.x_speed = None
        self.y_speed = None
        if abs(self.length[0]) > abs(self.length[1]):
            time = self.length[0] / self.speed
            self.y_speed = self.length[1] / time if self.length[0] > 0 else -(self.length[1] / time)
            self.float_speed = self.y_speed % 1 if self.y_speed > 0 else -(abs(self.y_speed) % 1)
        elif abs(self.length[0]) < abs(self.length[1]):
            time = self.length[1] / self.speed
            self.x_speed = self.length[0] / time if self.length[1] > 0 else -(self.length[0] / time)
            self.float_speed = self.x_speed % 1 if self.x_speed > 0 else -(abs(self.x_speed) % 1)

    def update(self):
        if self.y_speed:
            self.float_speed += self.y_speed % 1 if self.y_speed > 0 else -(abs(self.y_speed) % 1)
            self.rect = self.rect.move(self.speed if self.length[0] > 0 else -self.speed, self.y_speed)
            self.rect = self.rect.move(0, self.float_speed)
            if abs(self.float_speed) >= 1:
                self.float_speed = self.float_speed % 1 if self.y_speed > 0 else -(abs(self.float_speed) % 1)
        elif self.x_speed:
            self.float_speed += self.x_speed % 1 if self.x_speed > 0 else -(abs(self.x_speed) % 1)
            self.rect = self.rect.move(self.x_speed, self.speed if self.length[1] > 0 else -self.speed)
            self.rect = self.rect.move(self.float_speed, 0)
            if abs(self.float_speed) >= 1:
                self.float_speed = self.float_speed % 1 if self.x_speed > 0 else -(abs(self.float_speed) % 1)
        else:
            self.rect = self.rect.move(self.speed if self.length[0] > 0 else -self.speed,
                                       self.speed if self.length[1] > 0 else -self.speed)
