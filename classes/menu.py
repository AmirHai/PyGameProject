from AllConstants import *
from serviceFunctions import load_image, terminate
from Store import store


def menu_init(money, flag, items):
    money = money // 2
    buttons_sprites = pygame.sprite.Group()
    play_sprite = pygame.sprite.Sprite(buttons_sprites)
    play_sprite.image = pygame.transform.scale(load_image('play.png'), BUTTON_SIZE)
    play_sprite.rect = play_sprite.image.get_rect()
    play_sprite.rect.x = 450
    play_sprite.rect.y = 105
    store_sprite = pygame.sprite.Sprite(buttons_sprites)
    store_sprite.image = pygame.transform.scale(load_image('store.png'), BUTTON_SIZE)
    store_sprite.rect = store_sprite.image.get_rect()
    store_sprite.rect.x = 450
    store_sprite.rect.y = 310
    exit_sprite = pygame.sprite.Sprite(buttons_sprites)
    exit_sprite.image = pygame.transform.scale(load_image('exit.png'), BUTTON_SIZE)
    exit_sprite.rect = exit_sprite.image.get_rect()
    exit_sprite.rect.x = 450
    exit_sprite.rect.y = 515
    weapon = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return weapon, money * 2, items
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_sprite.rect.collidepoint(event.pos):
                    return weapon, money * 2, items
                if store_sprite.rect.collidepoint(event.pos):
                    new_weapon, money, items = store(money, flag, items)
                    if new_weapon:
                        weapon = new_weapon
                    flag = False
                if exit_sprite.rect.collidepoint(event.pos):
                    terminate()
        SCREEN.fill((47, 79, 79))
        buttons_sprites.draw(SCREEN)
        pygame.display.flip()
