from mainMenu import *
from AllConstants import *

if __name__ == '__main__':
    pygame.init()

    scrSize = WIDTH, HEIGHT
    screen = pygame.display.set_mode(scrSize)
    screen.fill(WHITE)

    menu = Menu()

    fps = 60
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(fps)
