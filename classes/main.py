from mainMenu import menu_init
from AllConstants import *
from serviceFunctions import terminate

if __name__ == '__main__':
    pygame.init()
    scrSize = WIDTH, HEIGHT
    screen = pygame.display.set_mode(scrSize)
    pygame.display.set_caption('Game')
    screen.fill('White')
    menu_init()
    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_init()
        SCREEN.fill('White')
        pygame.display.flip()
        CLOCK.tick(FPS)
