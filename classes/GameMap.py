from AllConstants import *


class GameMap:
    def __init__(self):
        self.board = [[0] * 100 for _ in range(100)]
        self.MainHeroPosition = [5.0, 5.0]
        for i in range(ROOMSIZE):
            for j in range(ROOMSIZE):
                if i == 0 or i == ROOMSIZE - 1 or j == 0 or j == ROOMSIZE - 1:
                    self.board[i][j] = 2
                else:
                    self.board[i][j] = 1

    def render(self):
        SCREEN.fill('Black')
        # тут происходит полная отрисовка карты, в котором цвета всех элементов изменятся в картинки
        for i in range(100):
            for j in range(100):
                x_change = CENTER[0] - round((self.MainHeroPosition[0] - i) * PIXELSIZE)
                y_change = CENTER[1] - round((self.MainHeroPosition[1] - j) * PIXELSIZE)
                if self.board[i][j] == 1:
                    pygame.draw.rect(SCREEN, (150, 150, 150), (x_change, y_change, PIXELSIZE, PIXELSIZE), 0)
                elif self.board[i][j] == 2:
                    pygame.draw.rect(SCREEN, (100, 100, 100), (x_change, y_change, PIXELSIZE, PIXELSIZE), 0)

        pygame.draw.rect(SCREEN, (0, 150, 0), (CENTER[0], CENTER[1], PIXELSIZE, PIXELSIZE), 0)
