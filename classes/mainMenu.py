from AllConstants import *
from serviceFunctions import load_image, terminate
from GameProcess import gameInit


def menu_init():
    buttons_sprites = pygame.sprite.Group()
    play_sprite = pygame.sprite.Sprite(buttons_sprites)
    play_sprite.image = pygame.transform.scale(load_image('play.png'), BUTTONSIZE)
    play_sprite.rect = play_sprite.image.get_rect()
    play_sprite.rect.x = 450
    play_sprite.rect.y = 60
    store_sprite = pygame.sprite.Sprite(buttons_sprites)
    store_sprite.image = pygame.transform.scale(load_image('store.png'), BUTTONSIZE)
    store_sprite.rect = store_sprite.image.get_rect()
    store_sprite.rect.x = 450
    store_sprite.rect.y = 240
    settings_sprite = pygame.sprite.Sprite(buttons_sprites)
    settings_sprite.image = pygame.transform.scale(load_image('settings.png'), BUTTONSIZE)
    settings_sprite.rect = settings_sprite.image.get_rect()
    settings_sprite.rect.x = 450
    settings_sprite.rect.y = 420
    exit_sprite = pygame.sprite.Sprite(buttons_sprites)
    exit_sprite.image = pygame.transform.scale(load_image('exit.png'), BUTTONSIZE)
    exit_sprite.rect = exit_sprite.image.get_rect()
    exit_sprite.rect.x = 450
    exit_sprite.rect.y = 600
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_sprite.rect.collidepoint(event.pos):
                    gameInit()
                if store_sprite.rect.collidepoint(event.pos):
                    pass
                if settings_sprite.rect.collidepoint(event.pos):
                    pass
                if exit_sprite.rect.collidepoint(event.pos):
                    terminate()
        SCREEN.fill('Black')
        buttons_sprites.draw(SCREEN)
        pygame.display.flip()
