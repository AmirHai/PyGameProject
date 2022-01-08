from main_menu import main_menu_init
from AllConstants import *

if __name__ == '__main__':
    pygame.init()
    scrSize = WIDTH, HEIGHT
    screen = pygame.display.set_mode(scrSize)
    pygame.display.set_caption('Game')
    main_menu_init()
