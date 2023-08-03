import os
import random
import pygame

#   Game Used Colours in RGB mode
white = (255, 255, 240)
red = (255, 0, 0)
black = (0, 0, 0)
mud_green = (52, 191, 152)
deep_green = (70, 137, 102)
light_yellow = (255, 240, 165)
mud_yellow = (255, 176, 59)
mud_red = (217, 43, 43)

#   Creating Window
screen_width = 600
screen_height = 400
gameWindow = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.init()
pygame.init()

#   BG Music
pygame.mixer.music.load("./media/bgsong.mp3")
pygame.mixer.music.play()

#   Background image
bgimg = pygame.image.load("./static/logo.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
set_icon = pygame.image.load("./static/icon.png")
pygame.display.set_icon(set_icon)

#   Game Title
pygame.display.set_caption("The Snake Master by Achyut Pal")
pygame.display.update()


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


#   Defining clock for time and will pass frame per second
clock = pygame.time.Clock()
#   Font Variable
font = pygame.font.SysFont(None, 40)


def score_text(text, color, x, y):
    text_score = font.render(text, True, color)
    gameWindow.blit(text_score, [x, y])


def welcome_screen():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(bgimg, (0, 0))
        score_text("Welcome to The Snake Master", white, 100, 40)
        score_text("Press Enter To Start", white, 180, 320)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load("./media/bgsong.mp3")
                    pygame.mixer.music.stop()
                    gameloop()
        pygame.display.update()
        clock.tick(5)


def game_rules():
    if not os.path.exists("./gamedata/game.txt"):
        with open("./gamedata/game.txt", "w") as f:
            f.write("""The Objective of the game is to Eat the Red Food.

                The more you eat, the Longer You Get and score Increases by +5.

                If you enter into yourself or the edges you Die!!!
                ------------------------------------------------------------------

                Game Controls-
                    Moving Keys - Up-Arrow, Down-Arrow, Right-Arrow, Left-Arrow
                    Pause/Quit - SpaceBar (Pause OR Restart), Q (Quit when Pause)""")


def pause():
    pause_game = True
    # score_text("Game Pauses!", black, 50, 150)
    while pause_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_game = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameWindow.fill(white)
        score_text("Game Pauses!", black, 50, 150)
        score_text("Space to resume or Q to quit ", black, 50, 200)
        clock.tick(5)
        pygame.display.update()


# Game loop
def gameloop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    #   Snake Position
    snake_x = 55
    snake_y = 65
    #   Snake Velocity
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    snake_size = 10  # rect size length and width
    snake_list = []
    snake_length = 1
    #   Food Position
    food_x = random.randint(100, screen_width-100)
    food_y = random.randint(100, screen_height-140)
    food_size = 12
    fps = 60  # frame per second
    # Game Score
    score = 0
    # Check ./gamedata/highscore.txt file exists or not in directory.
    game_rules()  # For Game rules
    if not os.path.exists("./gamedata/highscore.txt"):
        with open("./gamedata/highscore.txt", "w") as f:
            f.write("0")

    with open("./gamedata/highscore.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            with open("./gamedata/highscore.txt", "w") as f:
                f.write(str(high_score))
            gameWindow.fill(white)
            score_text("Game Over!!!  Press Enter To Restart.", black, 50, 150)
            score_text("Score " + str(score), mud_green, 20, 5)
            score_text("High Score " + str(high_score), mud_red, 350, 5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_SPACE:
                        pause()

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 5
                pygame.mixer.music.load("./media/food.mp3")
                pygame.mixer.music.play()
                if score > 500:
                    init_velocity += 1
                if score > 1500:
                    init_velocity += 1
                food_x = random.randint(20, screen_width-20)
                food_y = random.randint(20, screen_height-120)
                snake_length += 2
                if score > int(high_score):
                    high_score = score

            snake_head = []
            snake_head.append(snake_x)
            snake_head.append(snake_y)
            snake_list.append(snake_head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_head in snake_list[: -1]:
                game_over = True
                pygame.mixer.music.load("./media/over.mp3")
                pygame.mixer.music.play()

            gameWindow.fill(white)
            score_text("Score " + str(score), mud_green, 20, 5)
            score_text("High Score " + str(high_score), mud_red, 350, 5)
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("./media/over.mp3")
                pygame.mixer.music.play()
            plot_snake(gameWindow, black, snake_list, snake_size)
            pygame.draw.rect(gameWindow, red, [
                             food_x, food_y, food_size, food_size])
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome_screen()
