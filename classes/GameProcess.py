from GameMap import *
from Bullet import Bullet
from mainMenu import menu_init


def gameInit():
    gmap = GameMap()
    allkeys = [False] * 4
    buttons = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
    bullets_sprites = pygame.sprite.Group()
    bullet = None
    camera = Camera()
    while True:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(bullets_sprites, event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_init()
        PlayerSpeed = [0.0, 0.0]
        camera.update(0, 0)

        for i, bol in enumerate(allkeys):
            if bol:
                PlayerSpeed[i // 2 - 1] += 0.1 * (-1) ** (i % 2)
                gmap.MainHeroPosition = [gmap.MainHeroPosition[0] + PlayerSpeed[0],
                                         gmap.MainHeroPosition[1] + PlayerSpeed[1]]

        camera.update(round(PlayerSpeed[0] * 40), round(PlayerSpeed[1] * 40))
        for i in bullets_sprites:
            i.update()
            for j in gmap.allWalls:
                if pygame.sprite.collide_mask(i, j):
                    i.remove(bullets_sprites)
                    continue
        camera.apply(gmap.allWalls)
        camera.apply(gmap.allEmpty)
        if bullet:
            camera.apply(bullets_sprites)
        gmap.render()
        bullets_sprites.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)
