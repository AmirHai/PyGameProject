import pygame.sprite
import random

from GameMap import *
from Bullet import Bullet
from Monster import *
from menu import menu_init
from random import randrange


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

    running = True
    new_level = False

    Monsters_sprites = pygame.sprite.Group()

    for i in range(10):
        MonsterPos = random.choice(gmap.emptyKoordinates)
        Monster('swordsman', MonsterPos, gmap.MainHeroPosition, Monsters_sprites, level)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                for i, key in enumerate(buttons):
                    if event.key == key:
                        allkeys[i] = True
            if event.type == pygame.KEYUP:
                for i, key in enumerate(buttons):
                    if event.key == key:
                        allkeys[i] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                bought_item = menu_init()
                if bought_item:
                    weapons[1] = bought_item
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if weapons[1]:
                    weapons[0], weapons[1] = weapons[1], weapons[0]
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

        for i, bol in enumerate(allkeys):
            if bol:
                PlayerSpeed[i // 2 - 1] += 0.1 * (-1) ** (i % 2)
        PlayerSpeed = gmap.WallHelper(PlayerSpeed)

        gmap.MainHeroPosition = [round(gmap.MainHeroPosition[0] - PlayerSpeed[0], 2),
                                 round(gmap.MainHeroPosition[1] - PlayerSpeed[1], 2)]

        camera.update(round(PlayerSpeed[0] * 40), round(PlayerSpeed[1] * 40))

        for i in Monsters_sprites:
            i.moveToPlayer(gmap.MainHeroPosition)
            i.WallHelper(gmap.WallKoordinates)
            i.update()

        for i in bullets_sprites:
            i.update()
            for j in gmap.allWalls:
                if pygame.sprite.collide_mask(i, j):
                    i.remove(bullets_sprites)
                    continue
            for j in Monsters_sprites:
                if pygame.sprite.collide_mask(i, j):
                    if j.life == 1:
                        i.remove(bullets_sprites)
                        j.remove(Monsters_sprites)
                    else:
                        i.remove(bullets_sprites)
                        j.life -= 1

        for i in gmap.playerGroup:
            for j in Monsters_sprites:
                if pygame.sprite.collide_mask(i, j):
                    gmap.PlayerLife -= 1

        if len(Monsters_sprites) == 0:
            running = False
            new_level = True
        elif gmap.PlayerLife == 0:
            running = False
            new_level = False

        running_time += 1
        camera.apply(gmap.allWalls)
        camera.apply(gmap.allEmpty)
        camera.apply(Monsters_sprites)
        if bullet:
            camera.apply(bullets_sprites)
        gmap.render()
        weapons_sprites.draw(SCREEN)
        bullets_sprites.draw(SCREEN)
        Monsters_sprites.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)

    if new_level:
        return level + 1
    else:
        return level
