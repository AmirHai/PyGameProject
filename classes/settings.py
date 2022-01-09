from AllConstants import *
from serviceFunctions import terminate


def settings(difficulty):
    SCREEN.fill('Black')
    font = pygame.font.Font(None, 40)
    text = 'Выберите уровень сложности'
    text_rendered = font.render(text, True, 'White')
    text_rendered_rect = text_rendered.get_rect()
    text_rendered_rect.x = 437
    text_rendered_rect.y = 200
    difficulties = ['easy', 'normal', 'hard']
    difficulty_text = None
    if difficulty == 'easy':
        difficulty_text = 'Легко'
    elif difficulty == 'normal':
        difficulty_text = 'Нормально'
    elif difficulty == 'hard':
        difficulty_text = 'Сложно'
    difficulty_text_rendered = font.render(difficulty_text, True, 'White')
    difficulty_text_rendered_rect = difficulty_text_rendered.get_rect()
    difficulty_text_rendered_rect.x = 600
    difficulty_text_rendered_rect.y = 250
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if difficulty != 'easy':
                        difficulty = difficulties[difficulties.index(difficulty) - 1]
                        if difficulty == 'easy':
                            difficulty_text = 'Легко'
                        elif difficulty == 'normal':
                            difficulty_text = 'Нормально'
                        elif difficulty == 'hard':
                            difficulty_text = 'Сложно'
                        difficulty_text_rendered = font.render(difficulty_text, True, 'White')
                        SCREEN.fill('Black')
                if event.key == pygame.K_d:
                    if difficulty != 'hard':
                        difficulty = difficulties[difficulties.index(difficulty) + 1]
                        if difficulty == 'easy':
                            difficulty_text = 'Легко'
                        elif difficulty == 'normal':
                            difficulty_text = 'Нормально'
                        elif difficulty == 'hard':
                            difficulty_text = 'Сложно'
                        difficulty_text_rendered = font.render(difficulty_text, True, 'White')
                        SCREEN.fill('Black')
                if event.key == pygame.K_ESCAPE:
                    return difficulty
        difficulty_text_rendered_rect = difficulty_text_rendered.get_rect()
        difficulty_text_rendered_rect.x = 437
        difficulty_text_rendered_rect.y = 250
        pygame.display.flip()
        SCREEN.blit(text_rendered, text_rendered_rect)
        SCREEN.blit(difficulty_text_rendered, difficulty_text_rendered_rect)
