# Imports
import pygame
import random
import os
import sys
from pathlib import Path

# Initialize pygame
pygame.init()

# Initialize sound system
try:
    import pyxel
    # Initialize Pyxel with minimal settings (just for sound)
    pyxel.init(1, 1, fps=60, quit_key=None)
    
    # Create a simple background music
    pyxel.sound(0).set(
        "c3e3g3c4",  # notes
        "s",         # tone
        "3",         # volume
        "n",         # effect (none)
        20          # speed
    )
    
    # Play the music in loop
    pyxel.play(0, 0, loop=True)
except ImportError:
    print("Pyxel not available - running without sound")
except Exception as e:
    print(f"Sound initialization failed: {e} - running without sound")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40

# Colors (for fallback)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Game states
class GameState:
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3

def load_or_create_placeholder(image_path, color, size):
    """Load image or create a colored rectangle if image is missing"""
    try:
        if os.path.exists(image_path):
            img = pygame.image.load(image_path)
            return pygame.transform.scale(img, (size, size))
        else:
            # Try to generate assets
            from . import generate_assets
            generate_assets.generate_assets()
            
            # Try loading again
            if os.path.exists(image_path):
                img = pygame.image.load(image_path)
                return pygame.transform.scale(img, (size, size))
            else:
                surface = pygame.Surface((size, size))
                surface.fill(color)
                return surface
    except (pygame.error, ImportError) as e:
        print(f"Failed to load image {image_path}: {e}")
        surface = pygame.Surface((size, size))
        surface.fill(color)
        return surface

# Asset loading with fallback
assets_dir = Path(__file__).parent / "assets"
player_image = load_or_create_placeholder(assets_dir / "player.png", GREEN, TILE_SIZE)
monster_image = load_or_create_placeholder(assets_dir / "monster.png", RED, TILE_SIZE)
mustard_image = load_or_create_placeholder(assets_dir / "mustard.png", YELLOW, TILE_SIZE)
wall_image = load_or_create_placeholder(assets_dir / "wall.png", GRAY, TILE_SIZE)

def generate_maze(width, height):
    """Generate a maze with walls around the edges and some random internal walls"""
    maze = [[0 for _ in range(width)] for _ in range(height)]
    
    # Add walls around the edges
    for x in range(width):
        maze[0][x] = 1
        maze[height-1][x] = 1
    for y in range(height):
        maze[y][0] = 1
        maze[y][width-1] = 1
    
    # Add some random internal walls
    for y in range(1, height-1):
        for x in range(1, width-1):
            if random.random() < 0.2 and (x, y) != (1, 1):  # Keep starting position clear
                maze[y][x] = 1
                
    return maze

def is_valid_move(pos, maze):
    """Check if a position is valid (within bounds and not in a wall)"""
    grid_x = int(pos[0] // TILE_SIZE)
    grid_y = int(pos[1] // TILE_SIZE)
    if not (0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze)):
        return False
    return maze[grid_y][grid_x] != 1

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vibe Game")
clock = pygame.time.Clock()

def reset_game():
    """Reset game state"""
    global player_pos, monster_positions, mustard_pos, score, game_state, maze
    maze = generate_maze(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
    player_pos = [TILE_SIZE, TILE_SIZE]
    monster_positions = [[SCREEN_WIDTH - 2*TILE_SIZE, SCREEN_HEIGHT - 2*TILE_SIZE],
                        [SCREEN_WIDTH - 2*TILE_SIZE, TILE_SIZE]]
    
    # Make sure mustard spawns in a valid position
    while True:
        mustard_pos = [
            int(random.randint(1, (SCREEN_WIDTH // TILE_SIZE) - 2)) * TILE_SIZE,
            int(random.randint(1, (SCREEN_HEIGHT // TILE_SIZE) - 2)) * TILE_SIZE
        ]
        if is_valid_move(mustard_pos, maze):
            break
    
    return 0, GameState.PLAYING

# Initialize game state
score, game_state = reset_game()

# Font for text
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state == GameState.GAME_OVER:
                score, game_state = reset_game()
            elif event.key == pygame.K_p:
                if game_state == GameState.PLAYING:
                    game_state = GameState.PAUSED
                elif game_state == GameState.PAUSED:
                    game_state = GameState.PLAYING

    if game_state == GameState.PLAYING:
        # Player movement with collision detection
        keys = pygame.key.get_pressed()
        new_pos = player_pos.copy()
        
        move_speed = 5
        if keys[pygame.K_UP]:
            new_pos[1] -= move_speed
        if keys[pygame.K_DOWN]:
            new_pos[1] += move_speed
        if keys[pygame.K_LEFT]:
            new_pos[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            new_pos[0] += move_speed

        # Keep player within screen bounds
        new_pos[0] = max(0, min(new_pos[0], SCREEN_WIDTH - TILE_SIZE))
        new_pos[1] = max(0, min(new_pos[1], SCREEN_HEIGHT - TILE_SIZE))

        # Update position only if valid
        if is_valid_move(new_pos, maze):
            player_pos = new_pos

        # Monster movement with collision avoidance
        monster_speed = 2
        for monster in monster_positions:
            new_monster_pos = monster.copy()
            
            # Simple pathfinding
            dx = player_pos[0] - monster[0]
            dy = player_pos[1] - monster[1]
            
            # Normalize movement
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                dx = int((dx/dist) * monster_speed)
                dy = int((dy/dist) * monster_speed)
                
                # Try horizontal movement
                new_monster_pos[0] += dx
                if is_valid_move(new_monster_pos, maze):
                    monster[0] = new_monster_pos[0]
                
                # Try vertical movement
                new_monster_pos[1] += dy
                if is_valid_move(new_monster_pos, maze):
                    monster[1] = new_monster_pos[1]

        # Collision detection
        for monster in monster_positions:
            if (abs(player_pos[0] - monster[0]) < TILE_SIZE * 0.8 and 
                abs(player_pos[1] - monster[1]) < TILE_SIZE * 0.8):
                game_state = GameState.GAME_OVER

        # Mustard collection
        if (abs(player_pos[0] - mustard_pos[0]) < TILE_SIZE * 0.8 and 
            abs(player_pos[1] - mustard_pos[1]) < TILE_SIZE * 0.8):
            score += 100
            while True:
                mustard_pos = [
                    int(random.randint(1, (SCREEN_WIDTH // TILE_SIZE) - 2)) * TILE_SIZE,
                    int(random.randint(1, (SCREEN_HEIGHT // TILE_SIZE) - 2)) * TILE_SIZE
                ]
                if is_valid_move(mustard_pos, maze):
                    break

    # Drawing
    screen.fill(BLACK)
    
    # Draw maze
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 1:
                screen.blit(wall_image, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw game objects
    screen.blit(player_image, player_pos)
    for monster in monster_positions:
        screen.blit(monster_image, monster)
    screen.blit(mustard_image, mustard_pos)

    # Draw score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw game state messages
    if game_state == GameState.GAME_OVER:
        game_over_text = font.render('Game Over! Press R to Restart', True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, text_rect)
    elif game_state == GameState.PAUSED:
        pause_text = font.render('PAUSED - Press P to Continue', True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(pause_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
