# Aim Trainer Game

A simple Python game designed to help improve mouse accuracy and reaction time. Players must click fast-moving targets before they disappear.

## Features
- **Dynamic Targets**: Targets appear at random locations and grow/shrink in size.
- **Score Tracking**: Tracks hits, misses, and accuracy.
- **High Score**: Saves your best performance for the session.
- **Statistics**: Displays speed (targets per second) and accuracy percentage.

## Prerequisites
You need Python installed on your system. This game relies on the `pygame` library.

## Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone <your-repo-url>
    cd aim-trainer
    ```

2.  **Install dependencies**:
    ```bash
    pip install pygame
    ```

## How to Play

1.  **Run the game**:
    ```bash
    python AimTrainer.py
    ```

2.  **Start**: Click the "Start" button on the main menu.
3.  **Gameplay**:
    - Click on the red targets as they appear.
    - Targets will grow and then shrink. You must click them before they disappear.
    - The game lasts for a set duration (default: 20 seconds).
4.  **Game Over**:
    - Your stats (Speed, Hits, Accuracy, Misses) will be displayed.
    - Click "Restart" to try again.

## Controls
- **Mouse Left Click**: Interact with buttons and shoot targets.
- **Quit**: Close the window to exit the game.

## License
This project is open source and available for personal use.
