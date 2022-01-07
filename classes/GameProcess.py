import pygame.sprite
import random

from GameMap import *
from serviceFunctions import load_image
from Bullet import Bullet
from Monster import *
from menu import menu_init
from random import randrange
from endgame_Event import *

HEARTIMAGE = load_image('heart.png')


def gameInit(level):
    gmap = GameMap(level)
    allkeys = [False] * 4
    buttons = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    bullets_sprites = pygame.sprite.Group()
    bullet = None
    camera = Camera()
    weapons = ['pistol', None]
    weapons_sprites = pygame.sprite.Group()
    weapon = Weapon(weapons_sprites, weapons[0])
    running_time = 0

    cooldawn = 0
    monsterStopped = []

    gameRunning = True
    new_level = False

    Monsters_sprites = pygame.sprite.Group()

    # создание монстров
    for i in range(10):
        MonsterPos = random.choice(gmap.emptyKoordinates)
        Monster('swordsman', MonsterPos, gmap.MainHeroPosition, Monsters_sprites, level)
        monsterStopped.append(0)

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
                bought_item = menu_init()
                if bought_item:
                    weapons[1] = bought_item
            # смена оружия
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if weapons[1]:
                    weapons[0], weapons[1] = weapons[1], weapons[0]
        # стрельба
        if pygame.mouse.get_pressed()[0]:
            if running_time >= CUR.execute("""SELECT * FROM weapon_info WHERE name = ?""",
                                           (weapons[0],)).fetchall()[0][5]:
                pos = pygame.mouse.get_pos()
                if weapons[0] != 'shotgun':
                    bullet = Bullet(bullets_sprites, pos, weapons[0])
                else:
                    for i in range(8):
                        bullet = Bullet(bullets_sprites, (pos[0] + randrange(-25, 25),
                                                          pos[1] + randrange(-25, 25)), weapons[0])
                running_time = 0

        PlayerSpeed = [0.0, 0.0]
        camera.update(0, 0)

        # обработка передвижения персонажа
        for i, bol in enumerate(allkeys):
            if bol:
                PlayerSpeed[i // 2 - 1] += 0.15 * (-1) ** (i % 2)
        PlayerSpeed = gmap.WallHelper(PlayerSpeed)

        gmap.MainHeroPosition = [round(gmap.MainHeroPosition[0] - PlayerSpeed[0], 2),
                                 round(gmap.MainHeroPosition[1] - PlayerSpeed[1], 2)]

        camera.update(round(PlayerSpeed[0] * 40), round(PlayerSpeed[1] * 40))

        # обработка движения мобов
        for i, obj in enumerate(Monsters_sprites):
            if monsterStopped[i] == 0:
                obj.moveToPlayer(gmap.MainHeroPosition)
                obj.WallHelper(gmap.WallKoordinates)
                obj.update()
            elif monsterStopped[i] == 60:
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
                        obj.remove(Monsters_sprites)
                        monsterStopped.pop(j)
                    else:
                        i.remove(bullets_sprites)
                        obj.life -= 1
                        monsterStopped[j] = 1

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

        # обработка камеры и отрисовка поля
        camera.apply(gmap.allWalls)
        camera.apply(gmap.allEmpty)
        camera.apply(Monsters_sprites)
        if bullet:
            camera.apply(bullets_sprites)
        gmap.render()
        weapons_sprites.draw(SCREEN)
        bullets_sprites.draw(SCREEN)
        Monsters_sprites.draw(SCREEN)

        # увеличение показателя кулдауна моба
        for i in range(len(monsterStopped)):
            if monsterStopped[i] > 0:
                monsterStopped[i] += 1

        # отрисовка полоски здоровья
        for i in range(gmap.PlayerLife):
            heart = pygame.transform.scale(HEARTIMAGE, [25, 25])
            SCREEN.blit(heart, [10 + i * 30, 10])

        pygame.display.flip()
        CLOCK.tick(FPS)

    # проверка на проигрыш или выйгрыш 
    if new_level:
        endgameWin()
        return level + 1
    else:
        endgameLose()
        return level
