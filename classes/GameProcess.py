import pygame.sprite
import random

from GameMap import *
from serviceFunctions import load_image
from Bullet import Bullet
from Monster import *
from menu import menu_init
from random import randrange
from endgame_Event import *

ALLIMAGES = {
    'heart': load_image('heart.png'),
    'heroStanding': load_image('./characterGif/перс-аним1.png'),
    'heroMove1': load_image('./characterGif/перс-аним2.png'),
    'heroMove2': load_image('./characterGif/перс-аним3.png'),
    'skeletonStand': load_image('./SkeletonGif/скелет-аним1.png'),
    'skeletonMove1': load_image('./SkeletonGif/скелет-аним2.png'),
    'skeletonMove2': load_image('./SkeletonGif/скелет-аним3.png'),
}


def gameInit(level):
    startGameEvent(level)
    gmap = GameMap(level)
    allkeys = [False] * 4
    buttons = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    bullets_sprites = pygame.sprite.Group()
    camera = Camera()
    weapons = ['pistol', None]
    weapon_sprite = pygame.sprite.Group()
    Weapon(weapon_sprite, weapons[0])
    running_time = 0
    coins_collected = 0
    monstersKilled = 0
    first_store_opened = True
    store_items = []

    cooldawn = 0
    monsterStopped = []
    MonsterMove = []

    PlayerAnimation = 0

    gameRunning = True
    new_level = False

    Monsters_sprites = pygame.sprite.Group()
    coins_sprites = pygame.sprite.Group()

    # создание монстров
    for i in gmap.emptyKoordinates:
        if len(i) != 0:
            for _ in range(random.randint(5, 7)):
                MonsterPos = random.choice(i)
                Monster('swordsman', MonsterPos, gmap.MainHeroPosition, Monsters_sprites, level)
                monsterStopped.append(0)
                MonsterMove.append(False)

    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # проверка движения перонажа
            if event.type == pygame.KEYDOWN:
                for i, key in enumerate(buttons):
                    if event.key == key:
                        allkeys[i] = True
            if event.type == pygame.KEYUP:
                for i, key in enumerate(buttons):
                    if event.key == key:
                        allkeys[i] = False
            # покупка оружия
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                bought_item, coins_collected, store_items = menu_init(coins_collected,
                                                                      first_store_opened, store_items)
                if len(store_items) != 0:
                    first_store_opened = False
                if bought_item and bought_item != 'heal_potion':
                    weapons[1] = bought_item
                elif bought_item == 'heal_potion':
                    if gmap.PlayerLife <= 4:
                        gmap.PlayerLife += 2
                    elif gmap.PlayerLife == 5:
                        gmap.PlayerLife += 1

            # смена оружия
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if weapons[1]:
                    weapons[0], weapons[1] = weapons[1], weapons[0]
                    weapon_sprite = pygame.sprite.Group()
                    Weapon(weapon_sprite, weapons[0])
        # стрельба
        if pygame.mouse.get_pressed()[0]:
            if running_time >= CUR.execute("""SELECT * FROM weapon_info WHERE name = ?""",
                                           (weapons[0],)).fetchall()[0][5]:
                pos = pygame.mouse.get_pos()
                if weapons[0] != 'shotgun':
                    Bullet(bullets_sprites, pos, weapons[0])
                else:
                    for i in range(8):
                        Bullet(bullets_sprites, (pos[0] + randrange(-25, 25),
                                                 pos[1] + randrange(-25, 25)), weapons[0])
                running_time = 0

        PlayerSpeed = [0.0, 0.0]
        camera.update(0, 0)

        # обработка передвижения персонажа
        for i, bol in enumerate(allkeys):
            if bol:
                PlayerSpeed[i // 2 - 1] += 0.15 * (-1) ** (i % 2)
        PlayerSpeed = gmap.WallHelper(PlayerSpeed)

        if PlayerSpeed[0] == 0.0 and PlayerSpeed[1] == 0.0:
            for i in gmap.playerGroup:
                i.image = pygame.transform.scale(ALLIMAGES['heroStanding'], (40, 40))
        else:

            for i in gmap.playerGroup:
                if PlayerAnimation % 10 == 0:
                    i.image = pygame.transform.scale(ALLIMAGES['heroMove1'], (40, 40))

                if PlayerAnimation % 20 == 0:
                    i.image = pygame.transform.scale(ALLIMAGES['heroMove2'], (40, 40))

        gmap.MainHeroPosition = [round(gmap.MainHeroPosition[0] - PlayerSpeed[0], 2),
                                 round(gmap.MainHeroPosition[1] - PlayerSpeed[1], 2)]

        camera.update(round(PlayerSpeed[0] * 40), round(PlayerSpeed[1] * 40))

        # обработка движения мобов
        for i, obj in enumerate(Monsters_sprites):
            if monsterStopped[i] == 0:
                obj.moveToPlayer(gmap.MainHeroPosition)
                obj.WallHelper(gmap.WallKoordinates)
                if obj.speed[0] == 0.0 and obj.speed[1] == 0.0:
                    obj.image = pygame.transform.scale(ALLIMAGES['skeletonStand'], [25, 40])
                else:
                    if PlayerAnimation % 10 == 0:
                        obj.image = pygame.transform.scale(ALLIMAGES['skeletonMove1'], [40, 40])
                    if PlayerAnimation % 20 == 0:
                        obj.image = pygame.transform.scale(ALLIMAGES['skeletonMove2'], [40, 40])
                obj.update()
            elif monsterStopped[i] == 30:
                monsterStopped[i] = 0

        # обработка соприкосновений пуль со стеной и мобами
        for i in bullets_sprites:
            i.update()
            for j in gmap.allWalls:
                if pygame.sprite.collide_mask(i, j):
                    i.remove(bullets_sprites)
                    continue
            for j, obj in enumerate(Monsters_sprites):
                if pygame.sprite.collide_mask(i, obj):
                    if obj.life == 1:
                        i.remove(bullets_sprites)
                        rand = random.randint(0, 100)
                        if rand > 60:
                            Coin(coins_sprites, obj.position, gmap.MainHeroPosition)
                        obj.remove(Monsters_sprites)
                        monstersKilled += 1
                    else:
                        i.remove(bullets_sprites)
                        obj.life -= 1
                        monsterStopped[j] = 1

        for i in coins_sprites:
            for j in gmap.playerGroup:
                if pygame.sprite.collide_mask(i, j):
                    coins_collected += 1
                    i.remove(coins_sprites)

        # обработка прикосновения монстра с игроком
        for i in gmap.playerGroup:
            for j in Monsters_sprites:
                if pygame.sprite.collide_mask(i, j):
                    if cooldawn > FPS // 2:
                        gmap.PlayerLife -= 1
                        cooldawn = 0

        # проверка на проигрыш или выйгрыш
        if len(Monsters_sprites) == 0:
            gameRunning = False
            new_level = True
        elif gmap.PlayerLife == 0:
            gameRunning = False
            new_level = False

        running_time += 1
        cooldawn += 1
        PlayerAnimation += 1

        # обработка камеры и отрисовка поля
        camera.apply(gmap.allWalls)
        camera.apply(gmap.allEmpty)
        camera.apply(Monsters_sprites)
        camera.apply(coins_sprites)
        camera.apply(bullets_sprites)
        gmap.render()
        weapon_sprite.draw(SCREEN)
        bullets_sprites.draw(SCREEN)
        Monsters_sprites.draw(SCREEN)
        coins_sprites.draw(SCREEN)

        # увеличение показателя кулдауна моба
        for i in range(len(monsterStopped)):
            if monsterStopped[i] > 0:
                monsterStopped[i] += 1

        # отрисовка полоски здоровья
        for i in range(gmap.PlayerLife):
            heart = pygame.transform.scale(ALLIMAGES['heart'], [25, 25])
            SCREEN.blit(heart, [10 + i * 30, 10])

        # отрисовка количества монет
        font = pygame.font.Font(None, 35)
        text = font.render(f'{str(coins_collected)}', True, (200, 200, 200))
        SCREEN.blit(text, (20, 40))

        moneyImage = load_image('coin.png')
        moneyImage = pygame.transform.scale(moneyImage, (25, 25))
        SCREEN.blit(moneyImage, (50, 40))

        pygame.display.flip()
        CLOCK.tick(FPS)

    # проверка на проигрыш или выигрыш
    if new_level:
        endgameWin(monstersKilled, coins_collected)
        return level + 1
    else:
        endgameLose()
        return level
