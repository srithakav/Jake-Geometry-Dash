import pygame
import sys
import os
import random

# Initialize pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
background_image = pygame.image.load("neighborhood.png")
background_width = background_image.get_width() * 0.5
background_height = background_image.get_height()
SCREEN_WIDTH = background_width
SCREEN_HEIGHT = background_height

# Create the game window
screen = pygame.display.set_mode((background_width, background_height))
pygame.display.set_caption("State Farm Super Sprint")

# Background
background_image = pygame.image.load("neighborhood.png")
background_x = 0

# Music
pygame.mixer.music.load("statefarm2.mp3")
pygame.mixer_music.play()

# Player variables
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
initial_player_y = player_pos[1]
player_velocity = 0

# Gravity and jump variables
gravity = 0.5
jump_strength = -10

# Object variables
object_image = pygame.image.load("carcrash.png")
object_width = int(object_image.get_width() * 0.15)
object_height = int(object_image.get_height() * 0.15)
object_image = pygame.transform.scale(object_image, (object_width, object_height))
object_x = SCREEN_WIDTH
object_y = SCREEN_HEIGHT - object_height
object_speed = 5

# Climbing object variables
climbing_object_image = pygame.image.load("climbing_object.png")
climbing_object_width = 60
climbing_object_height = 20
climbing_object_image = pygame.transform.scale(climbing_object_image, (climbing_object_width, climbing_object_height))
climbing_object_x = SCREEN_WIDTH + 200
climbing_object_y = SCREEN_HEIGHT - player_size - climbing_object_height
climbing_object_speed = 5
climbing_object_direction = 1  # 1 for moving down, -1 for moving up

# Avoidant object variables
avoidant_objects = []

# Game variables
failed = False
welcome_screen = True

# Clock for time tracking
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# List to store top scores
# leaderboard = []

# Function to draw objects
def draw_objects():
    # Draw the objects
    screen.blit(object_image, (object_x, object_y))
    screen.blit(climbing_object_image, (climbing_object_x, climbing_object_y))

    # Draw the avoidant objects
    for avoidant_object in avoidant_objects:
        # coin = pygame.image.load("coin.png")
        # coin = pygame.transform.scale(coin, (80, 105))
        pygame.draw.rect(screen, RED, (avoidant_object["x"], avoidant_object["y"], avoidant_object["width"], avoidant_object["height"]))

# Function to update objects
def update_objects():
    global object_x, climbing_object_y, climbing_object_speed, climbing_object_direction

    object_x -= object_speed
    if object_x < -object_width:
        object_x = SCREEN_WIDTH

    climbing_object_y += climbing_object_speed * climbing_object_direction
    if climbing_object_y <= SCREEN_HEIGHT - player_size - climbing_object_height or climbing_object_y + climbing_object_height >= SCREEN_HEIGHT:
        climbing_object_direction *= -1

    for avoidant_object in avoidant_objects:
        avoidant_object["x"] -= avoidant_object["speed"]

        if avoidant_object["x"] < -avoidant_object["width"]:
            avoidant_objects.remove(avoidant_object)

        if avoidant_object["x"] < player_pos[0] < avoidant_object["x"] + avoidant_object["width"]:
            if avoidant_object["y"] <= player_pos[1] <= avoidant_object["y"] + avoidant_object["height"]:
                return True

    return False

# Function to check climbable collisions
def check_climbable_collisions():
    global player_velocity, player_pos, failed

    if player_pos[1] >= SCREEN_HEIGHT - player_size:
        player_velocity = 0

        if object_x < player_pos[0] < object_x + object_width:
            if object_y <= player_pos[1] <= object_y + object_height:
                failed = True

        if climbing_object_x < player_pos[0] < climbing_object_x + climbing_object_width:
            if climbing_object_y <= player_pos[1] <= climbing_object_y + climbing_object_height:
                player_velocity = 0
                player_pos[1] -= 2  # Move the player up (adjust as needed)

# Function to show the welcome screen
def show_welcome_screen():
    screen.fill(RED)

    font = pygame.font.Font("RetroGaming.ttf", 30)
    font1 = pygame.font.Font("RetroGaming.ttf", 24)
    title_text = font.render("Welcome to State Farm Super Sprint!", True, WHITE)
    instruction_text0 = font1.render(" " , True, WHITE)
    instruction_text1 = font1.render("Jake is embarking on a treacherous journey" , True, WHITE)
    instruction_text2 = font1.render("through a tornado to help policy holders." , True, WHITE)
    instruction_text3 = font1.render("Direct him away from the obstacles using" , True, WHITE)
    instruction_text4 = font1.render("the space bar. You never know what to" , True, WHITE)
    instruction_text5 = font1.render("expect so stay safe and get insured" , True, WHITE)
    instruction_text6 = font1.render(" by State Farm! Good luck!" , True, WHITE)
    instruction_text = font.render("Press SPACE to start", True, WHITE)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250))
    instruction_rect0 = instruction_text0.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-250 ))
    instruction_rect1 = instruction_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-200 ))
    instruction_rect2 = instruction_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-150 ))
    instruction_rect3 = instruction_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-100 ))
    instruction_rect4 = instruction_text4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-50 ))
    instruction_rect5 = instruction_text5.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
    instruction_rect6 = instruction_text6.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+50 ))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 +100))

    screen.blit(title_text, title_rect)
    screen.blit(instruction_text0, instruction_rect0)
    screen.blit(instruction_text1, instruction_rect1)
    screen.blit(instruction_text2, instruction_rect2)
    screen.blit(instruction_text3, instruction_rect3)
    screen.blit(instruction_text4, instruction_rect4)
    screen.blit(instruction_text5, instruction_rect5)
    screen.blit(instruction_text6, instruction_rect6)
    screen.blit(instruction_text, instruction_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# Function to display the leaderboard
# def display_leaderboard():
#     font = pygame.font.Font(None, 24)

#     leaderboard_text = font.render("Leaderboard:", True, RED)
#     screen.blit(leaderboard_text, (10, 10))

#     y_offset = 30
#     for i, score in enumerate(leaderboard[:5]):
#         score_text = font.render(f"{i+1}. {score}", True, RED)
#         screen.blit(score_text, (10, y_offset))
#         y_offset += 25

#     pygame.display.update()

# Main game loop
while True:
    if welcome_screen:
        show_welcome_screen()
        welcome_screen = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player_pos[1] >= initial_player_y:
        player_velocity = jump_strength
    elif keys[pygame.K_SPACE]:
        check_climbable_collisions()

    if failed:
        player_pos = [SCREEN_WIDTH // 2, initial_player_y]
        object_x = SCREEN_WIDTH
        object_y = SCREEN_HEIGHT - object_height
        climbing_object_x = SCREEN_WIDTH + 200
        climbing_object_y = SCREEN_HEIGHT - player_size - climbing_object_height
        player_velocity = 0
        failed = False
        avoidant_objects.clear()
        start_time = pygame.time.get_ticks()

        # Update leaderboard with the latest score
        # leaderboard.append(int((pygame.time.get_ticks() - start_time) / 1000))
        # leaderboard.sort(reverse=True)
        # if len(leaderboard) > 5:
        #     leaderboard = leaderboard[:5]

    player_velocity += gravity
    player_pos[1] += player_velocity

    check_climbable_collisions()

    if update_objects():
        failed = True

    # Update background position
    background_x -= 2  # Adjust the scrolling speed as needed
    if background_x <= -SCREEN_WIDTH:
        background_x = 0

    # Add new avoidant objects
    if len(avoidant_objects) < 5:
        avoidant_objects.append({
            "x": SCREEN_WIDTH,
            "y": random.randint(0, SCREEN_HEIGHT - player_size - climbing_object_height),
            "width": random.randint(30, 60),
            "height": random.randint(30, 60),
            "speed": random.randint(3, 8)
        })

    # Draw the background
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + SCREEN_WIDTH, 0))

    draw_objects()

    # Draw the player
    player = pygame.image.load("thursjake.png")
    player = pygame.transform.scale(player, (80, 105))
    screen.blit(player, (player_pos[0] - player_size // 2, (player_pos[1] - player_size // 2) - 75))
    # pygame.draw.rect(screen, RED, (player_pos[0] - player_size // 2, player_pos[1] - player_size // 2, player_size, player_size))

    # Draw the score on the screen
    font = pygame.font.Font(None, 36)
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display the leaderboard
    # display_leaderboard()

    pygame.display.update()
    clock.tick(60)
