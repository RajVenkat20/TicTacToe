# Starting point for the improvised Tic-Tac-Toe game.
# Run this file to open the Tic-Tac-Toe gui
from gui import TicTacToeGUI

if __name__ == "__main__":
    # By default, the board size is initialized to 3
    app = TicTacToeGUI(board_size=3)
    app.run()
