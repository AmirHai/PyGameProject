from serviceFunctions import *
from GameMap import *


def gameInit():
    allSprites = pygame.sprite.Group()
    Hero_sprite = pygame.sprite.Sprite(allSprites)
    Hero_sprite.image = pygame.transform.scale(load_image('character.png'), HEROSIZE)
    Hero_sprite.rect = Hero_sprite.image.get_rect()
    Hero_sprite.rect.x = CENTER[0]
    Hero_sprite.rect.y = CENTER[1]
    gmap = GameMap()
    allkeys = [False] * 4
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # копипаст чуть позже уберу))) >> AmirHai
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    allkeys[0] = True
                if event.key == pygame.K_s:
                    allkeys[1] = True
                if event.key == pygame.K_a:
                    allkeys[2] = True
                if event.key == pygame.K_d:
                    allkeys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    allkeys[0] = False
                if event.key == pygame.K_s:
                    allkeys[1] = False
                if event.key == pygame.K_a:
                    allkeys[2] = False
                if event.key == pygame.K_d:
                    allkeys[3] = False
        if allkeys[0]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0], gmap.MainHeroPosition[1] - 0.1]
        if allkeys[1]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0], gmap.MainHeroPosition[1] + 0.1]
        if allkeys[2]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0] - 0.1, gmap.MainHeroPosition[1]]
        if allkeys[3]:
            gmap.MainHeroPosition = [gmap.MainHeroPosition[0] + 0.1, gmap.MainHeroPosition[1]]
        gmap.render()
        pygame.display.flip()
        CLOCK.tick(FPS)
