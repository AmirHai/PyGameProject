from AllConstants import *
from serviceFunctions import load_image, terminate
from random import choice


def store(money, flag, items):
    SCREEN.fill('Black')
    if flag:
        all_items = CUR.execute("""SELECT * FROM weapon_info""").fetchall()
        items = []
        while len(items) != 3:
            random_item = choice(all_items)
            if random_item not in items and random_item[0] != 'pistol':
                items.append(random_item)
    items_sprites = pygame.sprite.Group()
    item1 = pygame.sprite.Sprite(items_sprites)
    item1.image = pygame.surface.Surface((0, 0))
    item1.rect = item1.image.get_rect()
    item2 = pygame.sprite.Sprite(items_sprites)
    item2.image = pygame.surface.Surface((0, 0))
    item2.rect = item2.image.get_rect()
    item3 = pygame.sprite.Sprite(items_sprites)
    item3.image = pygame.surface.Surface((0, 0))
    item3.rect = item3.image.get_rect()
    font = pygame.font.Font(None, 40)
    if items[0]:
        item1.image = pygame.transform.scale(load_image(items[0][0] + '.png'), STORE_ITEM_SIZE)
        item1.rect = item1.image.get_rect()
        item1.rect.x = 230
        item1.rect.y = 270
        text1_price = font.render(str(items[0][3]), True, 'White')
        text1_price_rect = text1_price.get_rect()
        text1_price_rect.x = 290
        text1_price_rect.y = 360
        SCREEN.blit(text1_price, text1_price_rect)
    if items[1]:
        item2.image = pygame.transform.scale(load_image(items[1][0] + '.png'), STORE_ITEM_SIZE)
        item2.rect = item2.image.get_rect()
        item2.rect.x = 580
        item2.rect.y = 270
        text2_price = font.render(str(items[1][3]), True, 'White')
        text2_price_rect = text2_price.get_rect()
        text2_price_rect.x = 640
        text2_price_rect.y = 360
        SCREEN.blit(text2_price, text2_price_rect)
    if items[2]:
        item3.image = pygame.transform.scale(load_image(items[2][0] + '.png'), STORE_ITEM_SIZE)
        item3.rect = item3.image.get_rect()
        item3.rect.x = 930
        item3.rect.y = 270
        text3_price = font.render(str(items[2][3]), True, 'White')
        text3_price_rect = text3_price.get_rect()
        text3_price_rect.x = 990
        text3_price_rect.y = 360
        SCREEN.blit(text3_price, text3_price_rect)
    retry = pygame.sprite.Sprite(items_sprites)
    retry.image = pygame.transform.scale(load_image('retry.png'), (60, 60))
    retry.rect = retry.image.get_rect()
    retry.rect.x = 1150
    retry.rect.y = 50
    text_retry = font.render('2', True, 'White')
    text_retry_rect = text_retry.get_rect()
    text_retry_rect.x = 1175
    text_retry_rect.y = 120
    SCREEN.blit(text_retry, text_retry_rect)
    text_money = font.render(str(money), True, 'White')
    text_money_rect = text_money.get_rect()
    text_money_rect.x = 10
    text_money_rect.y = 50
    SCREEN.blit(text_money, text_money_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None, money, items
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.rect.collidepoint(event.pos):
                    if money >= 2:
                        return store(money - 2, True, items)
                if item1.rect.collidepoint(event.pos):
                    if money >= items[0][3]:
                        return items[0][0], money - items[0][3], [None, items[1], items[2]]
                if item2.rect.collidepoint(event.pos):
                    if money >= items[1][3]:
                        return items[1][0], money - items[1][3], [items[0], None, items[2]]
                if item3.rect.collidepoint(event.pos):
                    if money >= items[2][3]:
                        return items[2][0], money - items[2][3], [items[0], items[1], None]
        items_sprites.draw(SCREEN)
        pygame.display.flip()
