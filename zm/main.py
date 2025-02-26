import pygame
import random

pygame.init()

# экрана
width = 700
height = 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zmeika")

# цвет
snake_color = (148, 0, 211)  # фиолетовый
apple_color = (0, 255, 0)    # зеленый


score_font = pygame.font.SysFont("Arial", 20)
game_clock = pygame.time.Clock()

# змейка
block_size = 20
speed = 5
snake_length = 3
snake_segments = []


for i in range(snake_length):
    snake_segments.append(pygame.Rect((width / 2) - (block_size * i), height / 2, block_size, block_size))

snake_move = "right"
next_move = "right"
apple_pos = pygame.Rect(random.randint(0, width - block_size), random.randint(0, height - block_size), block_size, block_size)

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_move != "down":
                next_move = "up"
            elif event.key == pygame.K_DOWN and snake_move != "up":
                next_move = "down"
            elif event.key == pygame.K_LEFT and snake_move != "right":
                next_move = "left"
            elif event.key == pygame.K_RIGHT and snake_move != "left":
                next_move = "right"

    # обнова направления движения
    snake_move = next_move

    # движение змейки
    if snake_move == "up":
        snake_segments.insert(0, pygame.Rect(snake_segments[0].left, snake_segments[0].top - block_size, block_size, block_size))
    elif snake_move == "down":
        snake_segments.insert(0, pygame.Rect(snake_segments[0].left, snake_segments[0].top + block_size, block_size, block_size))
    elif snake_move == "left":
        snake_segments.insert(0, pygame.Rect(snake_segments[0].left - block_size, snake_segments[0].top, block_size, block_size))
    elif snake_move == "right":
        snake_segments.insert(0, pygame.Rect(snake_segments[0].left + block_size, snake_segments[0].top, block_size, block_size))

    # яблоко съелось?
    if snake_segments[0].colliderect(apple_pos):
        apple_pos = pygame.Rect(random.randint(0, width - block_size), random.randint(0, height - block_size), block_size, block_size)
        snake_length += 1

    # обрезание хвост змейки, если она стала длиннее
    if len(snake_segments) > snake_length:
        snake_segments.pop()

    # проверка на столкновение со стеной
    if snake_segments[0].left < 0 or snake_segments[0].right > width or snake_segments[0].top < 0 or snake_segments[0].bottom > height:
        game_over = True

    # проверка на столкновение с телом змейки
    for segment in range(1, len(snake_segments)):
        if snake_segments[0].colliderect(snake_segments[segment]):
            game_over = True

    # очистка экран
    window.fill((0, 0, 0))

    # змейка
    for idx, segment in enumerate(snake_segments):
        if idx == 0:
            pygame.draw.circle(window, snake_color, segment.center, block_size / 2)
        else:
            pygame.draw.circle(window, snake_color, segment.center, block_size / 2)
            pygame.draw.circle(window, (148, 0, 211), segment.center, block_size / 4)

    # яблоко
    pygame.draw.circle(window, apple_color, apple_pos.center, block_size / 2)

    # счет
    score_text = score_font.render(f"Съедено яблок: {snake_length - 3}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.update()

    # контроль за частотой кадров
    game_clock.tick(speed)

pygame.quit()