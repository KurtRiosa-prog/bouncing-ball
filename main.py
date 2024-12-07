import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
BALL_COLOR = (255, 0, 0)  # This will no longer be used since we are using an image
BG_COLOR = (0, 0, 0)  # Background color (black for fallback)
PIPE_WIDTH = 80
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 220  # Gap between the pipes (Level 1)
PIPE_VELOCITY = 5  # Speed at which pipes move (Level 1)
FPS = 60
FONT = pygame.font.SysFont("Arial", 30)

# Set up screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Ball")
clock = pygame.time.Clock()

# Load background image
background = pygame.image.load("background.png")  # Replace with your image path
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the background to the screen size

# Load the ball image
ball_image = pygame.image.load("spaceship.png")  # Replace with your image path for the ball
ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))  # Scale image to fit ball size

# Ball starting position and speed
x = SCREEN_WIDTH // 4
y = SCREEN_HEIGHT // 2
speed_y = 0

# Pipe list
pipes = []

# Track score and high score
score = 0
high_score = 0

# Function to load and save high score to a file
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Function to create pipes (with shorter obstacles)
def create_pipe():
    height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 200)  # Make pipes shorter by reducing the upper limit
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_rect = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
    return top_rect, bottom_rect

# Function to check for collisions with pipes
def check_collisions(ball_rect, pipes):
    for top, bottom in pipes:
        if ball_rect.colliderect(top) or ball_rect.colliderect(bottom):
            return True
    return False

# Function to display the score, high score, and level
def display_score():
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 10))

# Function to display the current level
def display_level(level):
    level_text = FONT.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

# Function to display "Game Over" message
def display_game_over():
    font = pygame.font.SysFont("Arial", 50)
    game_over_text = font.render("GAME OVER", True, (20, 0, 0))
    restart_text = font.render("Press SPACE to Restart", True, (0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

# Function to reset the game to initial state
def reset_game():
    global x, y, speed_y, pipes, score, game_over, PIPE_VELOCITY, PIPE_GAP, level, GRAVITY
    x = SCREEN_WIDTH // 4
    y = SCREEN_HEIGHT // 2
    speed_y = 0
    pipes = []
    score = 0
    game_over = False
    PIPE_VELOCITY = 5  # Reset pipe velocity for Level 1
    PIPE_GAP = 220  # Reset pipe gap for Level 1
    GRAVITY = 0.5  # Reset gravity for Level 1
    level = 1  # Reset level to 1

# Load high score from file
high_score = load_high_score()

# Flag to track game over state
game_over = False

# Flag to track the level (Level 1 = 1, Level 2 = 2, Level 3 = 3)
level = 1

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # If game over and player presses space, restart the game
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()

        # Handle the flapping movement
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if not game_over:
                speed_y = FLAP_STRENGTH

    if game_over:
        # If the game is over, display the game over screen
        display_game_over()
        continue  # Skip the rest of the game loop

    # Update ball position
    speed_y += GRAVITY
    y += speed_y

    # Ball rectangle for collision detection
    ball_rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    # Check for collisions with pipes or the ground
    if check_collisions(ball_rect, pipes) or y + BALL_RADIUS > SCREEN_HEIGHT or y - BALL_RADIUS < 0:
        game_over = True
        # Update the high score if necessary
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    # Move pipes
    for top, bottom in pipes:
        top.x -= PIPE_VELOCITY
        bottom.x -= PIPE_VELOCITY

    # Remove pipes that have gone off-screen
    pipes = [pipe for pipe in pipes if pipe[0].x > -PIPE_WIDTH]

    # Create new pipes
    if len(pipes) == 0 or pipes[-1][0].x < SCREEN_WIDTH - 300:
        pipes.append(create_pipe())
        score += 1  # Increment score when a new pipe pair is passed

    # If the player reaches score 6, increase difficulty (Level 2)
    if score >= 6 and level == 1:
        level = 2
        PIPE_VELOCITY = 5  # Keep pipe speed the same for Level 2
        PIPE_GAP = 150  # Make the gap narrower in Level 2
        GRAVITY = 0.7  # Make the ball fall faster (slightly increased gravity)

    # If the player reaches score 12, increase difficulty (Level 3)
    if score >= 12 and level == 2:
        level = 3
        PIPE_VELOCITY = 6
        PIPE_GAP = 120  # Make the pipe gap even smaller in Level 3
        GRAVITY = 0.8  # Increase gravity (fall speed) further for Level 3

    # Choose pipe color based on level
    if level == 1:
        PIPE_COLOR = (225, 225, 0)  # yellow pipes for Level 1
    elif level == 2:
        PIPE_COLOR = (225, 165, 0)  # orange pipes for Level 2
    elif level == 3:
        PIPE_COLOR = (0, 255, 0)  # green pipes for Level 3

    # Fill screen with background image
    screen.blit(background, (0, 0))  # Draw the background image

    # Draw pipes
    for top, bottom in pipes:
        pygame.draw.rect(screen, PIPE_COLOR, top)
        pygame.draw.rect(screen, PIPE_COLOR, bottom)

    # Draw the ball (using the loaded image)
    screen.blit(ball_image, (x - BALL_RADIUS, y - BALL_RADIUS))

    # Display the current score, high score, and level
    display_score()
    display_level(level)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
