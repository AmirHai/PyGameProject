from serviceFunctions import *
from AllConstants import *

TYPES = {
    'swordsman': load_image('./SkeletonGif/скелет-аним1.png')
}


def into_speed(numb):
    if numb > 0:
        return 0.05
    elif numb < 0:
        return -0.05
    else:
        return 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, sprite_group, pos, player_pos):
        super().__init__(sprite_group)
        self.image = pygame.transform.scale(load_image('coin.png'), (PIXEL_SIZE * 0.5, PIXEL_SIZE * 0.5))
        self.mask = pygame.mask.from_surface(self.image)

        x_pos = CENTER[0] - (player_pos[0] - pos[0]) * PIXEL_SIZE
        y_pos = CENTER[1] - (player_pos[1] - pos[1]) * PIXEL_SIZE

        self.rect = self.image.get_rect().move(x_pos, y_pos)


class Monster(pygame.sprite.Sprite):
    def __init__(self, monster_type, position, player_pos, sprite_group, level, difficulty):
        super().__init__(sprite_group)
        self.image = pygame.transform.scale(TYPES[monster_type], (25, 40))

        x_pos = CENTER[0] - (player_pos[0] - position[0]) * PIXEL_SIZE
        y_pos = CENTER[1] - (player_pos[1] - position[1]) * PIXEL_SIZE

        self.rect = self.image.get_rect().move(x_pos, y_pos)
        self.position = position
        self.speed = None
        self.life = 4 * level
        if difficulty == 'hard':
            self.life += 2
        elif difficulty == 'easy':
            self.life -= 2

    def move_to_player(self, player_position):
        if abs(player_position[0] - self.position[0]) < MONSTER_VISION and \
                abs(player_position[1] - self.position[1]) < MONSTER_VISION:
            self.speed = [into_speed(player_position[0] - self.position[0]),
                          into_speed(player_position[1] - self.position[1])]
        else:
            self.speed = [0.0, 0.0]

    def wall_helper(self, walls_coord):
        if (int(self.position[0] + self.speed[0]), int(self.position[1])) in walls_coord:
            self.speed[0] = 0.0
        if (int(self.position[0]), int(self.position[1] + self.speed[1])) in walls_coord:
            self.speed[1] = 0.0

    def update(self):
        self.position = [round(self.position[0] + self.speed[0], 3),
                         round(self.position[1] + self.speed[1], 3)]
        self.rect = self.rect.move(self.speed[0] * PIXEL_SIZE, self.speed[1] * PIXEL_SIZE)
