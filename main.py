import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash")

# Player variables
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_velocity = 0

# Gravity and jump variables
gravity = 0.5
jump_strength = -10

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

    # Update player position and velocity
    player_velocity += gravity
    player_pos[1] += player_velocity

    # Collision detection with the ground
    if player_pos[1] >= SCREEN_HEIGHT - player_size:
        player_pos[1] = SCREEN_HEIGHT - player_size
        player_velocity = 0

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # Update the display
    pygame.display.update()