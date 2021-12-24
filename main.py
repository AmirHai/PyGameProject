import pygame

if __name__ == '__main__':
    pygame.init()

    scrSize = width, height = 1200, 800
    screen = pygame.display.set_mode(scrSize)
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Soul Knight: Главное меню')

    fps = 60
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
