# game_logic.py
BLANK_SQUARE = '_'

class TicTacToe:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.board = [BLANK_SQUARE] * (board_size ** 2)
        self.current_player = 'X'
        self.winner = None

    # Function to make a move on the board and shift turns among the players
    def make_move(self, position):
        if self.board[position] != BLANK_SQUARE or self.winner:
            return False
        self.board[position] = self.current_player
        self.winner = self.check_winner()
        if not self.winner:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    # Function that checks if the current board state results in the user winning or not
    def check_winner(self):
        size = self.board_size
        b = self.board

        # Check rows and columns
        for i in range(size):
            if b[i*size:(i+1)*size].count(b[i*size]) == size and b[i*size] != BLANK_SQUARE:
                return b[i*size]
            if [b[j*size + i] for j in range(size)].count(b[i]) == size and b[i] != BLANK_SQUARE:
                return b[i]

        # Check Diagonals
        if [b[i*(size+1)] for i in range(size)].count(b[0]) == size and b[0] != BLANK_SQUARE:
            return b[0]
        if [b[(i+1)*(size-1)] for i in range(size)].count(b[size-1]) == size and b[size-1] != BLANK_SQUARE:
            return b[size-1]

        return None

    # Function that checks if the board state results in a draw
    def is_draw(self):
        return BLANK_SQUARE not in self.board and not self.winner

    # Function to reset the current board state to the initial state
    def reset(self):
        self.board = [BLANK_SQUARE] * (self.board_size ** 2)
        self.current_player = 'X'
        self.winner = None
