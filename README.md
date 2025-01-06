# Space Invader Python

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat)](http://www.pygame.org/news.html)
[![Release](https://img.shields.io/badge/release-v2.0-orange.svg?style=flat)]()

## About
Space Invaders was the first fixed shooter and the first video game with endless gameplay, setting the template for the genre. The goal is to defeat wave after wave of descending aliens with a horizontally moving laser cannon to earn as many points as possible.

This version of Space Invaders introduces increasing difficulty: with each passing level, aliens move faster and fire lasers more frequently. To complete a level, the user must destroy all the aliens before they reach the obstacles, all while maintaining their three lives.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/space-invaders.git
   ```
2. Navigate to the project directory:
   ```bash
   cd space-invaders
   ```
3. Ensure you have Python installed on your system.
4. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## Files and Directories
The following files and directories are included in the `space-invaders` folder:
- **`game.py`**: Main game logic
- **`main.py`**: Entry point for running the game
- **`alien.py`**: Alien movement and behavior
- **`laser.py`**: Laser mechanics
- **`spaceship.py`**: Player spaceship controls
- **`obstacle.py`**: Obstacle interactions
- **`high_score.txt`**: Stores high scores
- **`Font/`**: Contains font resources
- **`Graphics/`**: Contains graphical assets
- **`Sounds/`**: Contains sound effects
- **`.gitattributes`**: Git configuration
- **`.venv/`**: Virtual environment for dependencies

## Running the Game
1. Ensure you are in the project directory:
   ```bash
   cd space-invaders
   ```
2. Run the main Python file to start the game:
   ```bash
   python main.py
   ```

## Controls
| Key         | Description         |
| :---------: | :-----------------: |
| `Arrow Keys`| Move                |
| `Space Bar` | Shoot Laser         |

## Gameplay
- With each level, the aliens increase slightly in movement speed and fire rate of lasers
- You have three lives to survive as long as possible

![Invader_Gameplay](https://github.com/user-attachments/assets/08a532e4-e762-4441-9789-e4bd64080382)
