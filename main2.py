import pygame
import sys
import os
import random

# Initialize pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
red = pygame.image.load("jakeywakey.gif")
background_image = pygame.image.load("neighborhood.png")
background_width = background_image.get_width()
background_height = background_image.get_height()
SCREEN_WIDTH = background_width
SCREEN_HEIGHT = background_height

# Create the game window
screen = pygame.display.set_mode((background_width, background_height))
pygame.display.set_caption("Geometry Dash")

# Background
background_image = pygame.image.load("neighborhood.png")
background_x = 0

# Player variables
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_velocity = 0

# Gravity and jump variables
gravity = 0.5
jump_strength = -10

# Object variables
object_image = pygame.image.load("object.png")
object_width = int(object_image.get_width() * 0.8)
object_height = int(object_image.get_height() * 0.8)
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

# Clock for time tracking
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and player_pos[1] >= SCREEN_HEIGHT - player_size:
        player_velocity = jump_strength

    # Restart the game if failed
    if failed:
        player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        object_x = SCREEN_WIDTH
        object_y = SCREEN_HEIGHT - object_height
        climbing_object_x = SCREEN_WIDTH + 200
        climbing_object_y = SCREEN_HEIGHT - player_size - climbing_object_height
        player_velocity = 0
        failed = False
        avoidant_objects.clear()
        start_time = pygame.time.get_ticks()

    # Update player position and velocity
    player_velocity += gravity
    player_pos[1] += player_velocity

    # Collision detection with the ground and objects
    if player_pos[1] >= SCREEN_HEIGHT - player_size:
        player_pos[1] = SCREEN_HEIGHT - player_size
        player_velocity = 0

        # Check for collision with objects
        if object_x < player_pos[0] < object_x + object_width:
            if object_y <= player_pos[1] <= object_y + object_height:
                failed = True

        # Check for collision with climbing object
        if climbing_object_x < player_pos[0] < climbing_object_x + climbing_object_width:
            if climbing_object_y <= player_pos[1] <= climbing_object_y + climbing_object_height:
                player_velocity = 0
                player_pos[1] -= 2  # Move the player up (adjust as needed)

    # Update background position
    background_x -= 2  # Adjust the scrolling speed as needed
    if background_x <= -SCREEN_WIDTH:
        background_x = 0

    # Update object positions
    object_x -= object_speed
    if object_x < -object_width:
        object_x = SCREEN_WIDTH

    # Update climbing object position
    climbing_object_y += climbing_object_speed * climbing_object_direction
    if climbing_object_y <= SCREEN_HEIGHT - player_size - climbing_object_height or climbing_object_y + climbing_object_height >= SCREEN_HEIGHT:
        climbing_object_direction *= -1

    # Update avoidant object positions and check for collisions
    for avoidant_object in avoidant_objects:
        avoidant_object["x"] -= avoidant_object["speed"]

        if avoidant_object["x"] < -avoidant_object["width"]:
            avoidant_objects.remove(avoidant_object)

        if avoidant_object["x"] < player_pos[0] < avoidant_object["x"] + avoidant_object["width"]:
            if avoidant_object["y"] <= player_pos[1] <= avoidant_object["y"] + avoidant_object["height"]:
                failed = True

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

    # Draw the objects
    screen.blit(object_image, (object_x, object_y))
    screen.blit(climbing_object_image, (climbing_object_x, climbing_object_y))

    # Draw the avoidant objects
    for avoidant_object in avoidant_objects:
        screen.blit(climbing_object_image, (avoidant_object["x"], avoidant_object["y"]))

    # Draw the player
    # avatar = pygame.image.load(os.path.join("images", "minecraftJake.png"))
    # pygame.display.set_icon(avatar)
    # pygame.image.save(screen, red)
    pygame.draw.rect(screen, RED, (player_pos[0] - player_size // 2, player_pos[1] - player_size // 2, player_size, player_size))

    # Update the score based on time elapsed
    score = int((pygame.time.get_ticks() - start_time) / 1000)

    # Draw the score on the screen
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)
