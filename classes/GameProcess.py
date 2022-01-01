from GameMap import *


def gameInit():
    gmap = GameMap()
    allkeys = [False] * 4
    buttons = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]

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
        camera.update(0, 0)
        if allkeys[0]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0], gmap.MainHeroPosition[1] - 0.1]
            camera.update(0, 4)
        if allkeys[1]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0], gmap.MainHeroPosition[1] + 0.1]
            camera.update(0, -4)
        if allkeys[2]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0] - 0.1, gmap.MainHeroPosition[1]]
            camera.update(4, 0)
        if allkeys[3]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0] + 0.1, gmap.MainHeroPosition[1]]
            camera.update(-4, 0)

        camera.apply(gmap.allWalls)
        camera.apply(gmap.allEmpty)

        gmap.render()
        pygame.display.flip()
        CLOCK.tick(FPS)
