# Vibe Game

A simple maze game where you collect mustard while avoiding monsters!

## Controls

- Arrow keys to move
- P to pause/unpause
- R to restart (when game over)

## Gameplay

- Navigate through the maze using arrow keys
- Collect yellow mustard items to score points (100 points each)
- Avoid the red monsters
- Game ends if a monster catches you

## Setup

1. Make sure you have Python 3.x installed
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python -m vibegame
   ```

## Custom Assets

The game will use colored rectangles by default, but you can add your own images:

1. Create an `assets` directory in the `src/vibegame` folder
2. Add the following PNG files:
   - `player.png`
   - `monster.png`
   - `mustard.png`
   - `wall.png`

The images will be automatically scaled to fit the game tiles. 