from AllConstants import *
from serviceFunctions import load_image, terminate
from GameProcess import game_init


def main_menu_init():
    buttons_sprites = pygame.sprite.Group()
    play_sprite = pygame.sprite.Sprite(buttons_sprites)
    play_sprite.image = pygame.transform.scale(load_image('play.png'), BUTTON_SIZE)
    play_sprite.rect = play_sprite.image.get_rect()
    play_sprite.rect.x = 450
    play_sprite.rect.y = 105
    settings_sprite = pygame.sprite.Sprite(buttons_sprites)
    settings_sprite.image = pygame.transform.scale(load_image('settings.png'), BUTTON_SIZE)
    settings_sprite.rect = settings_sprite.image.get_rect()
    settings_sprite.rect.x = 450
    settings_sprite.rect.y = 310
    exit_sprite = pygame.sprite.Sprite(buttons_sprites)
    exit_sprite.image = pygame.transform.scale(load_image('exit.png'), BUTTON_SIZE)
    exit_sprite.rect = exit_sprite.image.get_rect()
    exit_sprite.rect.x = 450
    exit_sprite.rect.y = 515

    level = 1
    items = ['pistol', None]
    money, all_money, killed = 0, 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_sprite.rect.collidepoint(event.pos):
                    new_level, items, money, all_money, killed = game_init(level, items,
                                                                           money, all_money, killed)
                    if level == 4 or new_level == level:
                        level = 1
                        items = ['pistol', None]
                        money, all_money, killed = 0, 0, 0
                    else:
                        level = new_level
                if settings_sprite.rect.collidepoint(event.pos):
                    pass
                if exit_sprite.rect.collidepoint(event.pos):
                    terminate()
        SCREEN.fill('Black')
        buttons_sprites.draw(SCREEN)
        pygame.display.flip()
