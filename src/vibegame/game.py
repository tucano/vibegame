import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Labyrinth")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player setup
player_pos = [TILE_SIZE, TILE_SIZE]
player_color = BLUE
player_speed = 5

# Maze setup (placeholder for dynamic maze generation)
maze = [[1 if random.random() > 0.8 else 0 for _ in range(SCREEN_WIDTH // TILE_SIZE)] for _ in range(SCREEN_HEIGHT // TILE_SIZE)]

# Mustard setup
mustard_color = YELLOW
mustard_pos = (
    random.randint(0, SCREEN_WIDTH // TILE_SIZE - 1) * TILE_SIZE,
    random.randint(0, SCREEN_HEIGHT // TILE_SIZE - 1) * TILE_SIZE
)

# Monster setup
monster_color = RED
monster_positions = [
    [random.randint(0, SCREEN_WIDTH // TILE_SIZE - 1) * TILE_SIZE,
     random.randint(0, SCREEN_HEIGHT // TILE_SIZE - 1) * TILE_SIZE]
    for _ in range(5)
]
monster_speed = 2

def check_collision(pos1, pos2):
    """Check if two positions collide."""
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def main():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        global player_pos
        keys = pygame.key.get_pressed()
        new_player_pos = player_pos[:]
        if keys[pygame.K_UP] and player_pos[1] > 0:
            new_player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - TILE_SIZE:
            new_player_pos[1] += player_speed
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            new_player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - TILE_SIZE:
            new_player_pos[0] += player_speed

        # Check collision with maze walls
        player_tile_x = new_player_pos[0] // TILE_SIZE
        player_tile_y = new_player_pos[1] // TILE_SIZE
        if maze[player_tile_y][player_tile_x] == 0:
            player_pos = new_player_pos

        # Monster movement (simple AI to chase player)
        for monster_pos in monster_positions:
            if monster_pos[0] < player_pos[0]:
                monster_pos[0] += monster_speed
            elif monster_pos[0] > player_pos[0]:
                monster_pos[0] -= monster_speed
            if monster_pos[1] < player_pos[1]:
                monster_pos[1] += monster_speed
            elif monster_pos[1] > player_pos[1]:
                monster_pos[1] -= monster_speed

        # Check collisions
        for monster_pos in monster_positions:
            if check_collision(player_pos, monster_pos):
                print("You were caught by a monster! Game Over.")
                running = False

        if check_collision(player_pos, mustard_pos):
            print("You reached the mustard! You win!")
            running = False

        # Drawing
        screen.fill(BLACK)

        # Draw maze
        for row_idx, row in enumerate(maze):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(screen, GRAY, (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw mustard
        pygame.draw.rect(screen, mustard_color, (*mustard_pos, TILE_SIZE, TILE_SIZE))

        # Draw monsters
        for monster_pos in monster_positions:
            pygame.draw.rect(screen, monster_color, (*monster_pos, TILE_SIZE, TILE_SIZE))

        # Draw player
        pygame.draw.rect(screen, player_color, (*player_pos, TILE_SIZE, TILE_SIZE))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()