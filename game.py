import pygame
import random

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Загрузка звукового эффекта
sound = pygame.mixer.Sound('Balloon.wav')

# Установка шрифта для рендеринга текста
font = pygame.font.Font(None, 36)

# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pin-pong')

# Размеры платформы
PLATFORM_WIDTH, PLATFORM_HEIGHT = 80, 10

# Создание прямоугольника для платформы игрока
player_platform = pygame.Rect(SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT - 10,
                              PLATFORM_WIDTH, PLATFORM_HEIGHT)

# Создание прямоугольника для мяча
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 30, 30)

# Определение цветов
ORANGE = (255, 171, 0)
WHITE = (255, 255, 255)

# Создание объекта Clock для управления скоростью кадров
clock = pygame.time.Clock()


def menu():
    """Отображение меню выбора скорости игры."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)

        # Рендеринг текста для кнопок
        slow_text = font.render('SLOW', True, WHITE)
        fast_text = font.render('FAST', True, WHITE)
        exit_text = font.render('EXIT', True, WHITE)

        # Создание прямоугольников для кнопок
        slow_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50)
        mouse_pos = pygame.mouse.get_pos()

        # Подсвечивание кнопки при наведении мыши
        if slow_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 0, 0), slow_btn)
        else:
            pygame.draw.rect(screen, (0, 0, 0), slow_btn)

        fast_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 260, 200, 50)
        if fast_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 0, 0), fast_btn)
        else:
            pygame.draw.rect(screen, (0, 0, 0), fast_btn)

        exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 50)

        if exit_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 0, 0), exit_btn)
        else:
            pygame.draw.rect(screen, (0, 0, 0), exit_btn)

        # Отображение текста на кнопках
        screen.blit(slow_text,
                    (slow_btn.centerx - slow_text.get_width() // 2, slow_btn.centery - slow_text.get_height() // 2))
        screen.blit(fast_text,
                    (fast_btn.centerx - fast_text.get_width() // 2, fast_btn.centery - fast_text.get_height() // 2))
        screen.blit(exit_text,
                    (exit_btn.centerx - exit_text.get_width() // 2, exit_btn.centery - exit_text.get_height() // 2))

        click = pygame.mouse.get_pressed()

        # Обработка событий при клике на кнопки
        if slow_btn.collidepoint(mouse_pos) and click[0]:
            return 4
        if fast_btn.collidepoint(mouse_pos) and click[0]:
            return 8
        if exit_btn.collidepoint(mouse_pos) and click[0]:
            pygame.quit()
            quit()

        pygame.display.update()


# Выбор скорости игры через меню
speed = menu()
ball_speed = [random.choice((-speed, speed)), -speed]  # [-5, 5]

score = 0
ball_collision = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Управление платформой игрока
    if keys[pygame.K_a] and player_platform.x > 0:
        player_platform.x -= speed
    elif keys[pygame.K_d] and player_platform.right < SCREEN_WIDTH:
        player_platform.x += speed

    # Движение мяча
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Обработка столкновений мяча с границами экрана
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] = - ball_speed[0]

    # Проверка, достиг ли мяч дна экрана
    if ball.bottom >= SCREEN_HEIGHT:
        ball.x = SCREEN_WIDTH // 2
        ball.y = SCREEN_HEIGHT // 2

        # Выбор скорости через меню
        speed = menu()
        ball_speed = [random.choice((-speed, speed)), -speed]

    # Обработка столкновений мяча с платформой игрока
    if ball.colliderect(player_platform) and not ball_collision:
        ball_speed[1] = -ball_speed[1]
        ball_collision = True
        sound.play()
        score += 1
    else:
        ball_collision = False

    # Отображение игровых объектов на экране
    screen.fill(ORANGE)

    score_text = font.render(f'Score: {score}', True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    pygame.draw.rect(screen, WHITE, player_platform)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
