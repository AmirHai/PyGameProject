import pygame
from time import sleep
from AllConstants import *
from serviceFunctions import *


# извините за копипаст, просто программа не правильно работала при выдаче текста из другого класса
def endgameWin():
    running = True
    textColor = (0, 0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        textColor = (textColor[0] + 1, textColor[1] + 1, textColor[2] + 1)
        font = pygame.font.Font(None, 60)
        text = font.render('You Win!!!', True, textColor)
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        SCREEN.blit(text, [text_x, text_y])
        if textColor[1] == 255:
            running = False
        pygame.display.flip()
        CLOCK.tick(FPS)


def endgameLose():
    running = True
    RedColor = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)
        if RedColor <= 100:
            text = font.render('You Died', False, (RedColor, 0, 0))
        else:
            text = font.render('You Died', False, (100, 0, 0))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        SCREEN.blit(text, [text_x, text_y])

        fontForMeme = pygame.font.Font(None, 20)
        meme = fontForMeme.render('да, это отсылка к Dark Souls)))', False, (75, 75, 75))
        SCREEN.blit(meme, [10, 10])

        if RedColor == 255:
            running = False
        RedColor += 1
        pygame.display.flip()
        CLOCK.tick(FPS)


def startGameEvent(level):
    running = True
    WhiteColor = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)

        text = font.render(f'Level {str(level)}', False, (WhiteColor, WhiteColor, WhiteColor))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        SCREEN.blit(text, [text_x, text_y])

        explanatoryTextFont = pygame.font.Font(None, 40)
        explanatoryText = explanatoryTextFont.render('You need to kill all monsters to win a game',
                                                     False, (WhiteColor, WhiteColor, WhiteColor))
        text_x = WIDTH // 2 - explanatoryText.get_width() // 2
        SCREEN.blit(explanatoryText, (text_x, text_y + 60))

        if WhiteColor == 255:
            running = False
        WhiteColor += 1
        pygame.display.flip()
        CLOCK.tick(FPS)
