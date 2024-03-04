"""
This script is a Pygame-based game where the player controls a dinosaur character
navigating through a series of obstacles. Pygame is a set of Python modules
designed for writing video games, providing functionalities for creating graphics,
sound, and handling user input.

Key Components:
1. Initialization: Pygame is initialized using `pygame.init()`, preparing the
   framework for use.

2. Game Settings: Global variables like `game_speed`, `x_pos_bg`, `y_pos_bg`,
   and `points` are defined for tracking game dynamics and scoring.

3. Main Game Loop: The `main` function contains the core game loop. This loop
   continuously checks for events (like key presses or the window closing),
   updates game state, and redraws the screen.

    a. Event Handling: Pygame's event system is used to respond to key presses
       and window closing events.
    b. Graphics Rendering: Game entities like the dinosaur, clouds, and obstacles
       are drawn onto the game window (`SCREEN`). Pygame functions like `blit`
       are used for drawing.
    c. Collision Detection: Pygame's rectangle collision feature is used to
       detect collisions between the dinosaur and obstacles.
    d. Scoring: Points are incremented based on game progress.

4. Game Pause and Unpause: Functions `paused` and `unpause` manage the game's
   pause state. During a pause, the game loop halts its usual update and draw
   cycle.

5. Background Management: The `background` function handles the scrolling
   background effect, giving a sense of movement.

6. Obstacle Management: Obstacles are dynamically generated and managed,
   offering variety and challenge in the gameplay.

7. Menu System: The `menu` function provides a start/restart interface and
   displays the player's score. It's also responsible for initiating the main
   game loop.

Pygame Functions:
- `pygame.init()`: Initializes all imported Pygame modules.
- `pygame.time.Clock()`: Creates an object to help track time.
- `clock.tick(fps)`: Limits the game loop to a maximum framerate.
- `pygame.display.update()`: Updates the contents of the entire display.
- `pygame.key.get_pressed()`: Gets the state of all keyboard buttons.
- `pygame.event.get()`: Retrieves all events from the event queue.
- `pygame.quit()`: Uninitializes all Pygame modules.
- `SCREEN.blit()`: Draws one image onto another.

This game is a simple yet engaging implementation demonstrating various aspects
of game development using Pygame, including graphics rendering, event handling,
collision detection, and game state management.
"""
from datetime import datetime

from resources import RUNNING, POWERUP, SPEEDUP
import pygame
import random
import threading
from settings import SCREEN_WIDTH, SCREEN, SCREEN_HEIGHT, GAME_SPEED
from dinosaur import Dinosaur, Dinosaur2
from cloud import Cloud
from obstacles import SmallCactus, LargeCactus, Bird, Powerup, Speedup
from resources import BG, SMALL_CACTUS, LARGE_CACTUS, BIRD

mp3_file_path = "Musik.mp3"
pygame.mixer.init()
pygame.mixer.music.load(mp3_file_path)
pygame.mixer.music.play()

# Initialize Pygame
pygame.init()

# List to store obstacles
obstacles = []


def load_highscore():
    with open('highscore.txt', 'r') as f:
        score = int(f.read())
        return int(score)

def is_dark_mode():
    now = datetime.now()
    # If it's later than 22:00 or earlier than 6:00, it's dark
    if now.hour >= 22 or now.hour > 6:
        return False
    return True

def save_highscore(points):
    with open("highscore.txt", "w") as f:
        f.write(str(points))


def main_menu():
    run = True
    selected = 0  # 0 for 'Start Game', 1 for 'Quit'
    pygame.init()

    while run:
        SCREEN.fill((0, 0, 0))  # Black background for the menu

        font = pygame.font.Font("freesansbold.ttf", 30)
        title = font.render("Dinosaur Game", True, FONT_COLOR)

        # Options text
        if selected == 0:
            start_game = font.render("Start Game <-", True, FONT_COLOR)
            quit_game = font.render("Quit", True, FONT_COLOR)
        else:
            start_game = font.render("Start Game", True, FONT_COLOR)
            quit_game = font.render("Quit <-", True, FONT_COLOR)

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        start_game_rect = start_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_game_rect = quit_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

        SCREEN.blit(title, title_rect)
        SCREEN.blit(start_game, start_game_rect)
        SCREEN.blit(quit_game, quit_game_rect)

        pygame.display.update()

        # Switch between the options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        run = False
                        main_anfang()
                    else:
                        pygame.quit()
                        quit()

def main_menu_multiplayer():
    run = True
    selected = 0  # 0 for 'Start Game', 1 for 'Quit'
    pygame.init()

    while run:
        SCREEN.fill((0, 0, 0))  # Black background for the menu

        font = pygame.font.Font("freesansbold.ttf", 30)
        title = font.render("Dinosaur Game", True, FONT_COLOR)

        # Options text
        if selected == 0:
            start_game = font.render("Coop Modus <-", True, FONT_COLOR)
            quit_game = font.render("Wettkampf Modus", True, FONT_COLOR)
        else:
            start_game = font.render("Coop Modus", True, FONT_COLOR)
            quit_game = font.render("Wettkampf Modus <-", True, FONT_COLOR)

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        start_game_rect = start_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_game_rect = quit_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

        SCREEN.blit(title, title_rect)
        SCREEN.blit(start_game, start_game_rect)
        SCREEN.blit(quit_game, quit_game_rect)

        pygame.display.update()

        # Switch between the options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        run = False
                        coop()
                    else:
                        multiplayer()
                        quit()
def main_anfang():
    run = True
    selected = 0  # 0 for 'Start Game', 1 for 'Quit'

    while run:
        SCREEN.fill((0, 0, 0))  # Black background for the menu

        font = pygame.font.Font("freesansbold.ttf", 30)
        title = font.render("Dinosaur Game", True, FONT_COLOR)

        # Options text
        if selected == 0:
            start_game = font.render("Singleplayer <-", True, FONT_COLOR)
            quit_game = font.render("Multiplayer", True, FONT_COLOR)
        else:
            start_game = font.render("Singleplayer", True, FONT_COLOR)
            quit_game = font.render("Multiplayer <-", True, FONT_COLOR)

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        start_game_rect = start_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_game_rect = quit_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

        SCREEN.blit(title, title_rect)
        SCREEN.blit(start_game, start_game_rect)
        SCREEN.blit(quit_game, quit_game_rect)

        pygame.display.update()

        # Switch between the options
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        run = False
                        main()
                    elif selected == 1:
                        run = False
                        main_menu_multiplayer()
def coop():
    # Global variables for game settings
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, Dinosaur2

    # Set initial game state
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    player2 = Dinosaur2()
    obstacles = []
    cloud = Cloud()
    game_speed = GAME_SPEED
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    death_count = 0
    pause = False



    # Function to handle scoring (currently empty)
    def score():
        global points, game_speed
        points +=1
        old_score = load_highscore()
        if old_score > points:
            save_highscore(old_score)
        else:
            save_highscore(points)

    # Function to handle background movement
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Function to unpause the game
    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    # Function to pause the game
    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    # Main game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused()

        dark_mode = is_dark_mode()

        if dark_mode:
            SCREEN.fill((30, 30, 30))  # Dark background
            FONT_COLOR = (255, 255,255)  # White font color

        else:
            SCREEN.fill((255, 255, 255))  # Standard background
            FONT_COLOR = (0, 0, 0)  # Black font color

        # Fill screen with white color
        #SCREEN.fill((255, 255, 255))

        # Get user input
        userInput = pygame.key.get_pressed()

        # Update and draw player and cloud
        player2.draw(SCREEN)
        player.draw(SCREEN)
        player.update(userInput)
        player2.update(userInput)
        cloud.draw(SCREEN)
        cloud.update()

        # Handle obstacles
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menumultiplayer(death_count)

            if player2.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menumultiplayer(death_count)


        # Update background and score
        background()
        score()

        # Update display and tick clock
        clock.tick(60)

        pygame.display.update()

def multiplayer():
    # Global variables for game settings
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, Dinosaur2

    # Set initial game state
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    player2 = Dinosaur2()
    obstacles = []
    cloud = Cloud()
    game_speed = GAME_SPEED
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    death_count = 0
    pause = False


    # Function to handle scoring (currently empty)
    def score():
        global points, game_speed
        points +=1
        old_score = load_highscore()
        if old_score > points:
            save_highscore(old_score)
        else:
            save_highscore(points)

    def score_player2():
        global points, game_speed
        points +=1
        old_score = load_highscore()
        if old_score > points:
            save_highscore(old_score)
        else:
            save_highscore(points)

    # Function to handle background movement
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Function to unpause the game
    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    # Function to pause the game
    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    # Main game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused()

        dark_mode = is_dark_mode()

        if dark_mode:
            SCREEN.fill((30, 30, 30))  # Dark background
            FONT_COLOR = (255, 255,255)  # White font color

        else:
            SCREEN.fill((255, 255, 255))  # Standard background
            FONT_COLOR = (0, 0, 0)  # Black font color

        # Fill screen with white color
        #SCREEN.fill((255, 255, 255))

        # Get user input
        userInput = pygame.key.get_pressed()

        # Update and draw player and cloud
        player2.draw(SCREEN)
        player.draw(SCREEN)
        player.update(userInput)
        player2.update(userInput)
        cloud.draw(SCREEN)
        cloud.update()

        score2 = score_player2()
        score2 = font.render("Second Player: " + str(points), True, FONT_COLOR)

        score2Rect = score2.get_rect()
        score2Rect.center = (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 300)
        SCREEN.blit(score2, score2Rect)

        score = font.render("First Player: " + str(points), True, FONT_COLOR)

        scoreRect = score.get_rect()
        scoreRect.center = (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 350)
        SCREEN.blit(score, scoreRect)

        #scoreRect = score.get_rect()
        #scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        #SCREEN.blit(score, scoreRect)

        # Handle obstacles
        if len(obstacles) == 0:
            if random.randint(0, 3) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 3) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 3) == 2:
                obstacles.append(Bird(BIRD))


        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menumultiplayer(death_count)

            if player2.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menumultiplayer(death_count)




        # Update background and score
        background()
        #score()

        # Update display and tick clock
        clock.tick(60)

        pygame.display.update()



def main():
    # Global variables for game settings
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles

    # Set initial game state
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    obstacles = []
    cloud = Cloud()
    game_speed = GAME_SPEED
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    death_count = 0
    pause = False


    # Function to handle scoring (currently empty)
    def score():
        global points, game_speed
        points +=1
        old_score = load_highscore()
        if old_score > points:
            save_highscore(old_score)
        else:
            save_highscore(points)

    # Function to handle background movement
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Function to unpause the game
    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    # Function to pause the game
    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    # Main game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused()

        dark_mode = is_dark_mode()

        if dark_mode:
            SCREEN.fill((30, 30, 30))  # Dark background
            FONT_COLOR = (255, 255, 255)  # White font color

        else:
            SCREEN.fill((255, 255, 255))  # Standard background
            FONT_COLOR = (0, 0, 0)  # Black font color
        # code f dark mode here
        # Fill screen with white color
        #SCREEN.fill((255, 255, 255))

        # Get user input
        userInput = pygame.key.get_pressed()

        # Update and draw player and cloud
        player.draw(SCREEN)
        player.update(userInput)
        cloud.draw(SCREEN)
        cloud.update()

        # Handle obstacles
        if len(obstacles) == 0:
            if random.randint(0, 4) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 4) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 4) == 2:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 4) == 3:
                obstacles.append(Powerup(POWERUP))
            elif random.randint(0 ,4) == 4:
                obstacles.append(Speedup(SPEEDUP))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update(obstacles)
            if  player.dino_rect.colliderect(obstacle.rect) and obstacle.__class__.__name__ == "Powerup":
                obstacles.remove(obstacle)
                player.jump_vel += 5
            elif player.dino_rect.colliderect(obstacle.rect) and obstacle.__class__.__name__ == "Speedup":
                obstacles.remove(obstacle)
                player.dino_run += 5
            elif player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        # Update background and score
        background()
        score()

        # Update display and tick clock
        clock.tick(60)

        pygame.display.update()



def menu(death_count):
    global points  # Access the global points variable to display the score.
    global FONT_COLOR  # Access the global font color variable for consistent text color.
    run = True  # Flag to keep the menu loop running.

    while run:
        FONT_COLOR = (255, 255, 255)  # Set the font color to white for visibility.
        SCREEN.fill((128, 128, 128))  # Fill the screen with a grey color as the background of the menu.
        pygame.font.init()  # Initialize Pygame font module.
        font = pygame.font.Font("freesansbold.ttf", 30)  # Set the font and size for the text.

        # Check if it's the start of the game or a restart after death.
        if death_count == 0:
            main_menu()



        elif death_count > 0:
            # Display a message to restart the game and the last score.
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            highscore = font.render("Your HighScore: " + str(load_highscore()), True, FONT_COLOR)

            highscoreRect = highscore.get_rect()
            highscoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(highscore, highscoreRect)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)  # Draw the score on the screen.
            SCREEN.blit(highscore, highscoreRect)  # Draw the score on the screen.

        # Render the text and position it on the screen.
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)  # Draw the text on the screen.

        # Display an image representing the game character.
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        pygame.display.update()  # Update the entire screen with everything drawn.

        # Event loop to handle window closing and key presses.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the window close button is clicked.
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Start the main game loop if any key is pressed.
                main_menu()
def menumultiplayer(death_count):
    global points  # Access the global points variable to display the score.
    global FONT_COLOR  # Access the global font color variable for consistent text color.
    run = True  # Flag to keep the menu loop running.

    while run:
        FONT_COLOR = (255, 255, 255)  # Set the font color to white for visibility.
        SCREEN.fill((128, 128, 128))  # Fill the screen with a grey color as the background of the menu.
        pygame.font.init()  # Initialize Pygame font module.
        font = pygame.font.Font("freesansbold.ttf", 30)  # Set the font and size for the text.

        # Check if it's the start of the game or a restart after death.
        if death_count == 0:
            main_menu()



        elif death_count > 0:
            # Display a message to restart the game and the last score.
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            highscore =  font.render("Your HighScore: " + str(load_highscore()), True, FONT_COLOR)
            highscoreRect = highscore.get_rect()
            highscoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(highscore, highscoreRect)
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)  # Draw the score on the screen.
            SCREEN.blit(highscore, highscoreRect)  # Draw the score on the screen.

        # Render the text and position it on the screen.
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)  # Draw the text on the screen.

        # Display an image representing the game character.
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        pygame.display.update()  # Update the entire screen with everything drawn.

        # Event loop to handle window closing and key presses.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the window close button is clicked.
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Start the main game loop if any key is pressed.
                main_menu()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
pygame.init()
t1.start()
