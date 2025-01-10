# Space Invader Python

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat)](http://www.pygame.org/news.html)
[![Release](https://img.shields.io/badge/release-v2.5-orange.svg?style=flat)]()

## About
Space Invaders was the first fixed shooter and the first video game with endless gameplay, setting the template for the genre. The goal is to see how long you can survive defeating wave after wave of descending aliens with a horizontally moving laser cannon while earning as many points as possible.
With each passing level aliens move faster and fire lasers more frequently. To complete a level, the player must destroy all the aliens before they either touch the obstacles or manage to take the player's three lives.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/navanateR/Space_Invader.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Space_Invader
   ```
3. Ensure you have Python installed on your system.
4. Install the required dependencies:
   ```bash
   pip install pygame
   ```
## Running the Game
1. Ensure you are in the project directory:
   ```bash
   cd Space_Invader
   ```
2. Run the main Python file to start the game:
   ```bash
   python main.py
   ```
   
## Files and Directories
The following files and directories are included in the `space-invaders` folder:
- **`game.py`**: Main game logic
- **`main.py`**: Entry point for running the game
- **`alien.py`**: Alien movement and behavior
- **`laser.py`**: Laser mechanics
- **`spaceship.py`**: Player spaceship controls
- **`obstacle.py`**: Obstacle interactions
- **`leaderboard.py`**: Handles high scores and the board
- **`leaderboard.json`**: Created at run to store score values
- **`Font/`**: Contains font resources
- **`Graphics/`**: Contains graphical assets
- **`Sounds/`**: Contains sound effects
- **`.gitattributes`**: Git configuration
- **`.venv/`**: Virtual environment for dependencies


## Controls
| Key         | Description         |
| :---------: | :-----------------: |
| `Arrow Keys`| Move                |
| `Space Bar` | Shoot Laser         |

## Gameplay
- In between each round you are able to position yourself before begining and the round wont begin until you press  the `Space Bar`
- After each attempt if your score was high enough to make the leaderboards you are prompted to enter three characters to secure your spot 
![Untitled design](https://github.com/user-attachments/assets/286a910a-5f63-4a44-b3bd-7028edff6942)


