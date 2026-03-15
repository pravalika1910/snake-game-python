import pygame
import random

pygame.init()

width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

white = (255,255,255)
black = (0,0,0)

snake_img = pygame.image.load("snake.png")
apple_img = pygame.image.load("apple.png")

snake_img = pygame.transform.scale(snake_img,(20,20))
apple_img = pygame.transform.scale(apple_img,(20,20))

snake_block = 20
snake_speed = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont(None,35)

# Load high score
try:
    file = open("highscore.txt","r")
    high_score = int(file.read())
    file.close()
except:
    high_score = 0

def save_high_score(score):
    file = open("highscore.txt","w")
    file.write(str(score))
    file.close()

def show_text(text,x,y):
    value = font.render(text,True,black)
    screen.blit(value,(x,y))

def game():

    global high_score

    x = width/2
    y = height/2

    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0,width-20)/20)*20
    foody = round(random.randrange(0,height-20)/20)*20

    pause = False
    game_over = False

    while not game_over:

        while pause:
            screen.fill(white)
            show_text("PAUSED - Press P to Continue",150,180)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0

                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0

                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0

                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

                elif event.key == pygame.K_p:
                    pause = True

        x += x_change
        y += y_change

        # Wall collision
        if x >= width or x < 0 or y >= height or y < 0:
            game_over = True

        screen.fill(white)

        screen.blit(apple_img,(foodx,foody))

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        for block in snake_list:
            screen.blit(snake_img,(block[0],block[1]))

        score = snake_length - 1

        show_text("Score: "+str(score),10,10)
        show_text("High Score: "+str(high_score),10,40)

        pygame.display.update()

        if x == foodx and y == foody:
            foodx = round(random.randrange(0,width-20)/20)*20
            foody = round(random.randrange(0,height-20)/20)*20
            snake_length += 1

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        clock.tick(snake_speed)

    # Game Over screen
    over = True

    while over:

        screen.fill(white)
        show_text("GAME OVER",250,150)
        show_text("Press R to Restart",220,200)
        show_text("Press Q to Quit",230,240)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    game()

                elif event.key == pygame.K_q:
                    over = False

    pygame.quit()

game()