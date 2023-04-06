import pygame
import random

# Initialize pygame
pygame.init()

# Set the screen size
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Define the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Define the functions for drawing the snake and the food
def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block_size, snake_block_size])

def draw_food(food_x, food_y, snake_block_size):
    pygame.draw.rect(screen, red, [food_x, food_y, snake_block_size, snake_block_size])

is_paused = False

clock = pygame.time.Clock()

eat_sound = pygame.mixer.Sound("sounds/eat.wav")
pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.set_volume(0.6)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_loop():
    global is_paused

    pygame.mixer.music.play(-1)

    # Set the snake's initial position and size
    snake_block_size = 10
    snake_speed = 15
    snake_list = []
    snake_length = 1
    snake_x = screen_width / 2
    snake_y = screen_height / 2

    # Generate the food position
    food_x = round(random.randrange(0, screen_width - snake_block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, screen_height - snake_block_size) / 10.0) * 10.0

    game_over = False

    key_pressed = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if ((event.key == pygame.K_LEFT and key_pressed != pygame.K_RIGHT) or
                    (event.key == pygame.K_RIGHT and key_pressed != pygame.K_LEFT) or
                    (event.key == pygame.K_UP and key_pressed != pygame.K_DOWN) or
                    (event.key == pygame.K_DOWN and key_pressed != pygame.K_UP)):
                        key_pressed = event.key

                if (event.key == pygame.K_ESCAPE):
                    is_paused = True
                    paused()

        if key_pressed == pygame.K_LEFT:
            snake_x -= snake_block_size
        elif key_pressed == pygame.K_RIGHT:
            snake_x += snake_block_size
        elif key_pressed == pygame.K_UP:
            snake_y -= snake_block_size
        elif key_pressed == pygame.K_DOWN:
            snake_y += snake_block_size

        # Update the snake length and position
        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if the snake hits the wall or itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True
        if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
            game_over = True

        # Check if the snake eats the food
        if snake_x == food_x and snake_y == food_y:
            pygame.mixer.Sound.play(eat_sound)
            food_x = round(random.randrange(0, screen_width - snake_block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, screen_height - snake_block_size) / 10.0) * 10.0
            snake_length += 1

        # Draw the snake and the food
        screen.fill(white)
        draw_snake(snake_block_size, snake_list)
        draw_food(food_x, food_y, snake_block_size)
        pygame.display.update()

        # Set the game speed
        clock.tick(snake_speed)

def paused():
    global is_paused

    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((screen_width/2),(screen_height/2))
    screen.blit(TextSurf, TextRect)

    while is_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.unpause()
                is_paused = False

        pygame.display.update()
        clock.tick(15)  


game_loop()
pygame.quit()
