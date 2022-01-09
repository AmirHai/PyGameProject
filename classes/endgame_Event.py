from AllConstants import *
from serviceFunctions import *


# извините за копипаст, просто программа не правильно работала при выдаче текста из другого класса
def endgame_win(mobs_killed, coins_collected):
    running = True
    text_color = (0, 0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        text_color = (text_color[0] + 1, text_color[1] + 1, text_color[2] + 1)
        font = pygame.font.Font(None, 60)
        text = font.render('You Win!!!', True, text_color)
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        SCREEN.blit(text, [text_x, text_y])

        font_info = pygame.font.Font(None, 40)
        text_info = font_info.render(f'Monsters Killed: {str(mobs_killed)} Coins '
                                     f'collected: {str(coins_collected)}', True, text_color)
        text_x = WIDTH // 2 - text_info.get_width() // 2
        SCREEN.blit(text_info, (text_x, text_y + 60))

        if text_color[1] == 255:
            running = False
        pygame.display.flip()
        CLOCK.tick(FPS)


def endgame_lose():
    running = True
    red_color = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)
        if red_color <= 100:
            text = font.render('You Died', False, (red_color, 0, 0))
        else:
            text = font.render('You Died', False, (100, 0, 0))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        SCREEN.blit(text, [text_x, text_y])

        font_for_meme = pygame.font.Font(None, 20)
        meme = font_for_meme.render('да, это отсылка к Dark Souls)))', False, (75, 75, 75))
        SCREEN.blit(meme, [10, 10])

        if red_color == 255:
            running = False
        red_color += 1
        pygame.display.flip()
        CLOCK.tick(FPS)


def start_game_event(level):
    running = True
    white_color = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)

        text = font.render(f'Level {str(level)}', False, (white_color, white_color, white_color))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        SCREEN.blit(text, [text_x, text_y])

        explanatory_text_font = pygame.font.Font(None, 40)
        explanatory_text = explanatory_text_font.render('You need to kill all monsters to win a game',
                                                        False, (white_color, white_color, white_color))
        text_x = WIDTH // 2 - explanatory_text.get_width() // 2
        SCREEN.blit(explanatory_text, (text_x, text_y + 60))

        if white_color == 255:
            running = False
        white_color += 1
        pygame.display.flip()
        CLOCK.tick(FPS)
