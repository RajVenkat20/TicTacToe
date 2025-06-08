# TicTacToe 🎮

A simple two-player Tic-Tac-Toe game built with Python and Tkinter.

## 🧱 Repository Structure

TicTacToe/
├── game_logic.py # Core game logic: handles move validation, win/tie detection, player switching, and reset functionality.
├── gui.py # GUI layer: builds the window, board display, buttons, and ties button clicks to game logic.
├── main.py # Entry point: creates TicTacToeGame, injects into GUI, and launches the application.
└── pycache/ # Auto-generated cache — you can ignore or gitignore this folder.

## 🚀 How to Run

1. **Ensure you have Python 3.x installed**, along with Tkinter (usually included by default).  
   On Ubuntu/Debian:  
   ```bash
   sudo apt-get install python3-tk
   ```

2. Clone this repository(or download):
   ```bash
   git clone https://github.com/RajVenkat20/TicTacToe.git
   cd TicTacToe
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. A window will appear with the Tic-Tac-Toe board. Two players can take turns clicking cells to play.
