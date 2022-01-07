from AllConstants import *
from serviceFunctions import load_image, terminate
from random import choice


def store():
    all_items = CUR.execute("""SELECT * FROM weapon_info""").fetchall()
    items = []
    while len(items) != 3:
        random_item = choice(all_items)
        if random_item not in items:
            items.append(random_item)
    items_sprites = pygame.sprite.Group()
    item1 = pygame.sprite.Sprite(items_sprites)
    item1.image = pygame.transform.scale(load_image('pistol.png'), STOREITEMSIZE)
    item1.rect = item1.image.get_rect()
    item1.rect.x = 230
    item1.rect.y = 270
    item2 = pygame.sprite.Sprite(items_sprites)
    item2.image = pygame.transform.scale(load_image('pistol.png'), STOREITEMSIZE)
    item2.rect = item2.image.get_rect()
    item2.rect.x = 580
    item2.rect.y = 270
    item3 = pygame.sprite.Sprite(items_sprites)
    item3.image = pygame.transform.scale(load_image('pistol.png'), STOREITEMSIZE)
    item3.rect = item3.image.get_rect()
    item3.rect.x = 930
    item3.rect.y = 270
    prices = [i[3] for i in items]
    font = pygame.font.Font(None, 40)
    prices_text = []
    x = 290
    for i in prices:
        textr = font.render(str(i), True, 'White')
        intro_rect = textr.get_rect()
        intro_rect.x = x
        intro_rect.y = 360
        prices_text.append((textr, intro_rect))
        x += 350
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if item1.rect.collidepoint(event.pos):
                    return items[0][0]
                if item2.rect.collidepoint(event.pos):
                    return items[1][0]
                if item3.rect.collidepoint(event.pos):
                    return items[2][0]
        SCREEN.fill('Black')
        for i in prices_text:
            SCREEN.blit(i[0], i[1])
        items_sprites.draw(SCREEN)
        pygame.display.flip()
