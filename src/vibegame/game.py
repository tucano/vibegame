# Imports
import pygame
import random
import os
import sys
from pathlib import Path
import pyxel

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40

# Colors
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

# Create and play 8-bit style loop music with Pyxel
def create_music():
    # Initialize Pyxel with no display (just for sound)
    pyxel.init(1, 1, fps=30, quit_key=None)

    # Define music patterns (8-bit style with mayo accents)
    pyxel.sound(0).set(
        "c3e3g3c4 c4g3e3c3 f3a3c4f4 f4c4a3f3",  # Notes
        "p",  # Tone (piano-like)
        "7",  # Volume
        "n",  # Effect (no effect)
        25,   # Speed
    )
    pyxel.sound(1).set(
        "g2b2d3g3 g3d3b2g2 a2c3e3a3 a3e3c3a2",  # Notes
        "t",  # Tone (triangle wave for bass)
        "7",  # Volume
        "n",  # Effect (no effect)
        25,   # Speed
    )
    pyxel.sound(2).set(
        "c4d4e4f4 g4a4b4c5 d5e5f5g5 a5b5c6d6",  # Valid notes (mayo accents)
        "s",  # Tone (square wave for sharp accents)
        "6",  # Volume
        "f",  # Effect (fade)
        50,   # Speed
    )

    # Combine sounds into a music loop
    pyxel.music(0).set(
        (0, 1, 2, 0),  # Sound channels
        "nnnn",        # Play all channels normally
        30,            # Speed
    )

    # Play the music loop indefinitely
    pyxel.playm(0, loop=True)

# Call the function to create and play music
create_music()

def load_or_create_placeholder(image_path, color, size):
    """Load image or create a colored rectangle if image is missing"""
    try:
        if os.path.exists(image_path):
            img = pygame.image.load(image_path)
            return pygame.transform.scale(img, (size, size))
        else:
            surface = pygame.Surface((size, size))
            surface.fill(color)
            return surface
    except pygame.error:
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
    maze = [[0 for x in range(width)] for y in range(height)]
    
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
    grid_x = pos[0] // TILE_SIZE
    grid_y = pos[1] // TILE_SIZE
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
        mustard_pos = [random.randint(1, (SCREEN_WIDTH // TILE_SIZE) - 2) * TILE_SIZE,
                      random.randint(1, (SCREEN_HEIGHT // TILE_SIZE) - 2) * TILE_SIZE]
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
        
        if keys[pygame.K_UP]:
            new_pos[1] -= 5
        if keys[pygame.K_DOWN]:
            new_pos[1] += 5
        if keys[pygame.K_LEFT]:
            new_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            new_pos[0] += 5

        # Update position only if valid
        if is_valid_move(new_pos, maze):
            player_pos = new_pos

        # Monster movement with collision avoidance
        for monster in monster_positions:
            new_monster_pos = monster.copy()
            
            # Simple pathfinding
            dx = player_pos[0] - monster[0]
            dy = player_pos[1] - monster[1]
            
            # Normalize movement
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                dx = (dx/dist) * 2
                dy = (dy/dist) * 2
                
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
                mustard_pos = [random.randint(1, (SCREEN_WIDTH // TILE_SIZE) - 2) * TILE_SIZE,
                              random.randint(1, (SCREEN_HEIGHT // TILE_SIZE) - 2) * TILE_SIZE]
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
