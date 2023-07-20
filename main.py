import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player
PLAYER_SIZE = 50
PLAYER_Y = HEIGHT - PLAYER_SIZE - 10
PLAYER_VY = 0
GRAVITY = 1

# Obstacle
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 100
OBSTACLE_X = WIDTH
OBSTACLE_SPEED = 10

def draw_window(window, player_rect, obstacle_rect):
    window.fill(WHITE)
    pygame.draw.rect(window, RED, player_rect)
    pygame.draw.rect(window, RED, obstacle_rect)
    pygame.display.update()

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player_rect = pygame.Rect(WIDTH / 4, PLAYER_Y, PLAYER_SIZE, PLAYER_SIZE)
    obstacle_rect = pygame.Rect(OBSTACLE_X, HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and player_rect.y == PLAYER_Y:
                if event.key == pygame.K_SPACE:
                    PLAYER_VY = -20

        if player_rect.y < PLAYER_Y:
            PLAYER_VY += GRAVITY
        else:
            player_rect.y = PLAYER_Y
            PLAYER_VY = 0

        player_rect.y += PLAYER_VY
        obstacle_rect.x -= OBSTACLE_SPEED

        if obstacle_rect.right < 0:
            obstacle_rect.x = WIDTH

        if player_rect.colliderect(obstacle_rect):
            pygame.quit()
            sys.exit()

        draw_window(window, player_rect, obstacle_rect)

if __name__ == "__main__":
    main()