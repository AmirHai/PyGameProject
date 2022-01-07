from mainMenu import menu_init
from AllConstants import *
from GameProcess import gameInit

if __name__ == '__main__':
    pygame.init()
    scrSize = WIDTH, HEIGHT
    screen = pygame.display.set_mode(scrSize)
    pygame.display.set_caption('Game')
    menu_init()
