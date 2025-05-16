import pygame
import os
from pathlib import Path

def create_surface(size, main_color, accent_color=None):
    """Create a surface with a basic pixel art design"""
    surface = pygame.Surface((size, size))
    surface.fill((0, 0, 0, 0))  # Transparent background
    
    # Draw main shape
    padding = size // 8
    rect = pygame.Rect(padding, padding, size - 2*padding, size - 2*padding)
    pygame.draw.rect(surface, main_color, rect)
    
    # Add accent if provided
    if accent_color:
        accent_size = size // 4
        accent_rect = pygame.Rect(
            size//2 - accent_size//2,
            size//2 - accent_size//2,
            accent_size,
            accent_size
        )
        pygame.draw.rect(surface, accent_color, accent_rect)
    
    return surface

def generate_assets():
    """Generate game assets"""
    pygame.init()
    
    # Asset size
    size = 64  # Size for the original assets before scaling
    
    # Create assets directory if it doesn't exist
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Generate player (green with blue accent)
    player = create_surface(size, (0, 200, 0), (0, 0, 200))
    pygame.image.save(player, assets_dir / "player.png")
    
    # Generate monster (red with dark accent)
    monster = create_surface(size, (200, 0, 0), (100, 0, 0))
    pygame.image.save(monster, assets_dir / "monster.png")
    
    # Generate mustard (yellow with orange accent)
    mustard = create_surface(size, (255, 255, 0), (255, 165, 0))
    pygame.image.save(mustard, assets_dir / "mustard.png")
    
    # Generate wall (gray with darker accent)
    wall = create_surface(size, (128, 128, 128), (64, 64, 64))
    pygame.image.save(wall, assets_dir / "wall.png")
    
    pygame.quit()

if __name__ == "__main__":
    generate_assets() 