import pygame.sprite
import random

from GameMap import *
from Bullet import Bullet
from Monster import *
from menu import menu_init
from random import randrange
from endgame_Event import *

ALL_IMAGES = {
    'heart': load_image('heart.png'),
    'heroStanding': load_image('./characterGif/перс-аним1.png'),
    'heroMove1': load_image('./characterGif/перс-аним2.png'),
    'heroMove2': load_image('./characterGif/перс-аним3.png'),
    'skeletonStand': load_image('./SkeletonGif/скелет-аним1.png'),
    'skeletonMove1': load_image('./SkeletonGif/скелет-аним2.png'),
    'skeletonMove2': load_image('./SkeletonGif/скелет-аним3.png'),
}


def game_init(level, weapons, coins_collected, all_coins_collected, monsters_killed, difficulty):
    start_game_event(level)
    game_map = GameMap(level)
    all_keys = [False] * 4
    buttons = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    bullets_sprites = pygame.sprite.Group()
    camera = Camera()
    weapon_sprite = pygame.sprite.Group()
    Weapon(weapon_sprite, weapons[0])
    running_time = 0
    first_store_opened = True
    store_items = []

    cooldown = 0
    monster_stopped = []
    monster_move = []

    player_animation = 0

    game_running = True
    new_level = False

    monsters_sprites = pygame.sprite.Group()
    coins_sprites = pygame.sprite.Group()

    # создание монстров
    for i in game_map.empty_coordinates:
        if len(i) != 0:
            for _ in range(random.randint(5, 7)):
                monster_pos = random.choice(i)
                Monster('swordsman', monster_pos, game_map.MainHeroPosition,
                        monsters_sprites, level, difficulty)
                monster_stopped.append(0)
                monster_move.append(False)

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # проверка движения перонажа
            if event.type == pygame.KEYDOWN:
                for i, key in enumerate(buttons):
                    if event.key == key:
                        all_keys[i] = True
            if event.type == pygame.KEYUP:
                for i, key in enumerate(buttons):
                    if event.key == key:
                        all_keys[i] = False
            # покупка оружия
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                bought_item, coins_collected, store_items = menu_init(coins_collected,
                                                                      first_store_opened, store_items)
                if len(store_items) != 0:
                    first_store_opened = False
                if bought_item and bought_item != 'heal_potion':
                    weapons[1] = bought_item
                elif bought_item == 'heal_potion':
                    if game_map.PlayerLife <= 4:
                        game_map.PlayerLife += 2
                    elif game_map.PlayerLife == 5:
                        game_map.PlayerLife += 1

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

        player_speed = [0.0, 0.0]
        camera.update(0, 0)

        # обработка передвижения персонажа
        for i, bol in enumerate(all_keys):
            if bol:
                player_speed[i // 2 - 1] += 0.2 * (-1) ** (i % 2)
        player_speed = game_map.wall_helper(player_speed)

        if player_speed[0] == 0.0 and player_speed[1] == 0.0:
            for i in game_map.playerGroup:
                i.image = pygame.transform.scale(ALL_IMAGES['heroStanding'], (40, 40))
        else:

            for i in game_map.playerGroup:
                if player_animation % 10 == 0:
                    i.image = pygame.transform.scale(ALL_IMAGES['heroMove1'], (40, 40))

                if player_animation % 20 == 0:
                    i.image = pygame.transform.scale(ALL_IMAGES['heroMove2'], (40, 40))

        game_map.MainHeroPosition = [round(game_map.MainHeroPosition[0] - player_speed[0], 2),
                                     round(game_map.MainHeroPosition[1] - player_speed[1], 2)]

        camera.update(round(player_speed[0] * 40), round(player_speed[1] * 40))

        # обработка движения мобов
        for i, obj in enumerate(monsters_sprites):
            if monster_stopped[i] == 0:
                obj.move_to_player(game_map.MainHeroPosition)
                obj.wall_helper(game_map.wall_coordinates)
                if obj.speed[0] == 0.0 and obj.speed[1] == 0.0:
                    obj.image = pygame.transform.scale(ALL_IMAGES['skeletonStand'], [25, 40])
                else:
                    if player_animation % 10 == 0:
                        obj.image = pygame.transform.scale(ALL_IMAGES['skeletonMove1'], [40, 40])
                    if player_animation % 20 == 0:
                        obj.image = pygame.transform.scale(ALL_IMAGES['skeletonMove2'], [40, 40])
                obj.update()
            elif monster_stopped[i] == 30:
                monster_stopped[i] = 0

        # обработка соприкосновений пуль со стеной и мобами
        for i in bullets_sprites:
            i.update()
            for j in game_map.allWalls:
                if pygame.sprite.collide_mask(i, j):
                    i.remove(bullets_sprites)
                    continue
            for j, obj in enumerate(monsters_sprites):
                if pygame.sprite.collide_mask(i, obj):
                    damage = CUR.execute("""SELECT * FROM weapon_info WHERE name = ?""",
                                         (weapons[0],)).fetchall()[0][4]
                    if obj.life - damage <= 0:
                        i.remove(bullets_sprites)
                        rand = random.randint(0, 100)
                        if rand > 60:
                            Coin(coins_sprites, obj.position, game_map.MainHeroPosition)
                        obj.remove(monsters_sprites)
                        monsters_killed += 1
                    else:
                        i.remove(bullets_sprites)
                        obj.life -= damage
                        monster_stopped[j] = 1

        for i in coins_sprites:
            for j in game_map.playerGroup:
                if pygame.sprite.collide_mask(i, j):
                    coins_collected += 1
                    all_coins_collected += 1
                    i.remove(coins_sprites)

        # обработка прикосновения монстра с игроком
        for i in game_map.playerGroup:
            for j in monsters_sprites:
                if pygame.sprite.collide_mask(i, j):
                    if cooldown > FPS // 2:
                        game_map.PlayerLife -= 1
                        cooldown = 0

        # проверка на проигрыш или выигрыш
        if len(monsters_sprites) == 0:
            game_running = False
            new_level = True
        elif game_map.PlayerLife == 0:
            game_running = False
            new_level = False

        running_time += 1
        cooldown += 1
        player_animation += 1

        # обработка камеры и отрисовка поля
        camera.apply(game_map.allWalls)
        camera.apply(game_map.allEmpty)
        camera.apply(monsters_sprites)
        camera.apply(coins_sprites)
        camera.apply(bullets_sprites)
        game_map.render()
        weapon_sprite.draw(SCREEN)
        bullets_sprites.draw(SCREEN)
        monsters_sprites.draw(SCREEN)
        coins_sprites.draw(SCREEN)

        # увеличение показателя кулдауна моба
        for i in range(len(monster_stopped)):
            if monster_stopped[i] > 0:
                monster_stopped[i] += 1

        # отрисовка полоски здоровья
        for i in range(game_map.PlayerLife):
            heart = pygame.transform.scale(ALL_IMAGES['heart'], [25, 25])
            SCREEN.blit(heart, [10 + i * 30, 10])

        # отрисовка количества монет
        font = pygame.font.Font(None, 35)
        text = font.render(str(coins_collected // 2), True, (200, 200, 200))
        SCREEN.blit(text, (20, 40))
        money_image = load_image('coin.png')
        money_image = pygame.transform.scale(money_image, (25, 25))
        SCREEN.blit(money_image, (50, 40))

        pygame.display.flip()
        CLOCK.tick(FPS)

    # проверка на проигрыш или выигрыш
    if new_level:
        endgame_win(monsters_killed, all_coins_collected // 2)
        return level + 1, weapons, coins_collected, all_coins_collected, monsters_killed
    else:
        endgame_lose()
        return level, weapons, coins_collected, all_coins_collected, monsters_killed
