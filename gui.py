import tkinter as tk
import random
from tkinter import messagebox
from game_logic import TicTacToe


class TicTacToeGUI:
    def __init__(self, board_size=3):
        # These game variables are global and are used across various functions
        self.board_size = board_size
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("800x700")
        self.game_frame = None
        self.player_names = {}
        self.buttons = []
        self.status_label = None
        self.game = None
        self.landing_screen()

    def landing_screen(self):
        landing = tk.Frame(self.root)
        landing.pack(expand=True)

        title_frame = tk.Frame(landing)
        title_frame.pack(pady=30)

        tk.Label(title_frame, text="Tic", font=("Comic Sans MS", 36, "bold"), fg="red").pack(side=tk.LEFT)
        tk.Label(title_frame, text="-Tac-", font=("Comic Sans MS", 36, "bold"), fg="black").pack(side=tk.LEFT)
        tk.Label(title_frame, text="Toe", font=("Comic Sans MS", 36, "bold"), fg="blue").pack(side=tk.LEFT)


        btn1 = tk.Button(landing, text="Play with AI", font=("Helvetica", 16), width=30, pady=10,
                 command=lambda: self.ask_ai_setup(landing))
        btn1.pack(pady=10)

        btn2 = tk.Button(landing, text="Single Game", font=("Helvetica", 16),
                        width=30, pady=10, command=lambda: self.ask_player_names(landing))
        btn2.pack(pady=10)

        btn3 = tk.Button(landing, text="Best of 3 or 5", font=("Helvetica", 16),
                        width=30, pady=10,
                        command=lambda: self.ask_match_setup(landing))
        btn3.pack(pady=10)

        quit_btn = tk.Button(landing, text="Quit", font=("Helvetica", 16), width=30, pady=10,
                            command=self.root.destroy)
        quit_btn.pack(pady=20)

    def ask_player_names(self, landing_frame):
        landing_frame.destroy()
        name_frame = tk.Frame(self.root)
        name_frame.pack(expand=True, pady=30)

        tk.Label(name_frame, text="Enter Game Setup", font=("Comic Sans MS", 24, "bold")).pack(pady=10)

        tk.Label(name_frame, text="Player 1 (X):", font=("Helvetica", 14)).pack()
        p1_entry = tk.Entry(name_frame, font=("Helvetica", 14))
        p1_entry.pack(pady=5)

        tk.Label(name_frame, text="Player 2 (O):", font=("Helvetica", 14)).pack()
        p2_entry = tk.Entry(name_frame, font=("Helvetica", 14))
        p2_entry.pack(pady=5)

        tk.Label(name_frame, text="Board Size (e.g., 3 for 3x3):", font=("Helvetica", 14)).pack()
        size_entry = tk.Entry(name_frame, font=("Helvetica", 14))
        size_entry.insert(0, "3")
        size_entry.pack(pady=5)

        def start():
            p1 = p1_entry.get().strip() or "Player 1"
            p2 = p2_entry.get().strip() or "Player 2"

            try:
                size = int(size_entry.get().strip())
                if size < 2:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Board Size", "Please enter a valid number (2 or higher).")
                return

            name_frame.destroy()
            self.board_size = size  # Set board size dynamically
            self.start_multiplayer_game(p1, p2)

        btn_frame = tk.Frame(name_frame)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame, text="Start Match", font=("Helvetica", 14), width=15,
            command=start
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame, text="Return to Home", font=("Helvetica", 14), width=15,
            command=lambda: [name_frame.destroy(), self.landing_screen()]
        ).pack(side=tk.LEFT, padx=10)
        
    def ask_match_setup(self, landing_frame):
        landing_frame.destroy()
        setup_frame = tk.Frame(self.root)
        setup_frame.pack(expand=True, pady=30)

        tk.Label(setup_frame, text="Match Setup", font=("Comic Sans MS", 24, "bold")).pack(pady=10)

        # Player Names
        tk.Label(setup_frame, text="Player 1 (X):", font=("Helvetica", 14)).pack()
        p1_entry = tk.Entry(setup_frame, font=("Helvetica", 14))
        p1_entry.pack(pady=5)

        tk.Label(setup_frame, text="Player 2 (O):", font=("Helvetica", 14)).pack()
        p2_entry = tk.Entry(setup_frame, font=("Helvetica", 14))
        p2_entry.pack(pady=5)

        # Board Size
        tk.Label(setup_frame, text="Board Size: (e.g., 3 for 3x3)", font=("Helvetica", 14)).pack()
        size_entry = tk.Entry(setup_frame, font=("Helvetica", 14))
        size_entry.insert(0, "3")
        size_entry.pack(pady=5)

        # Best of 3 or 5
        tk.Label(setup_frame, text="Match Type:", font=("Helvetica", 14)).pack()
        match_type = tk.StringVar(value="3")
        tk.Radiobutton(setup_frame, text="Best of 3", variable=match_type, value="3", font=("Helvetica", 12)).pack()
        tk.Radiobutton(setup_frame, text="Best of 5", variable=match_type, value="5", font=("Helvetica", 12)).pack()

        def start_match():
            p1 = p1_entry.get().strip() or "Player 1"
            p2 = p2_entry.get().strip() or "Player 2"

            try:
                size = int(size_entry.get().strip())
                if size < 2:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Board Size", "Please enter a valid number (2 or higher).")
                return

            self.board_size = size
            self.total_games = int(match_type.get())
            self.current_game = 1
            self.player_names = {'X': p1, 'O': p2}
            self.scores = {'X': 0, 'O': 0}

            setup_frame.destroy()
            self.start_match_game()

        btn_frame = tk.Frame(setup_frame)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame, text="Start Match", font=("Helvetica", 14), width=15,
            command=start_match
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame, text="Return to Home", font=("Helvetica", 14), width=15,
            command=lambda: [setup_frame.destroy(), self.landing_screen()]
        ).pack(side=tk.LEFT, padx=10)

    def ask_ai_setup(self, landing_frame):
        landing_frame.destroy()
        ai_frame = tk.Frame(self.root)
        ai_frame.pack(expand=True, pady=30)

        tk.Label(ai_frame, text="Play Against AI", font=("Comic Sans MS", 24, "bold")).pack(pady=10)

        # Player name input
        tk.Label(ai_frame, text="Your Name (X):", font=("Helvetica", 14)).pack()
        player_entry = tk.Entry(ai_frame, font=("Helvetica", 14))
        player_entry.pack(pady=5)

        # Board size input
        tk.Label(ai_frame, text="Board Size (e.g., 3 for 3x3):", font=("Helvetica", 14)).pack()
        size_entry = tk.Entry(ai_frame, font=("Helvetica", 14))
        size_entry.insert(0, "3")
        size_entry.pack(pady=5)

        # Difficulty selection
        tk.Label(ai_frame, text="Select Difficulty:", font=("Helvetica", 14)).pack(pady=10)
        difficulty = tk.StringVar(value="Easy")
        tk.Radiobutton(ai_frame, text="Easy", variable=difficulty, value="Easy", font=("Helvetica", 12)).pack()
        tk.Radiobutton(ai_frame, text="Hard", variable=difficulty, value="Hard", font=("Helvetica", 12)).pack()

        def start_game():
            player_name = player_entry.get().strip() or "You"
            try:
                size = int(size_entry.get().strip())
                if size < 2:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Board Size", "Enter a valid number (2 or higher).")
                return

            self.board_size = size
            self.player_names = {'X': player_name, 'O': "AI"}
            ai_frame.destroy()
            self.start_ai_game(difficulty.get())  # Pass "Easy" or "Hard"


        btn_frame = tk.Frame(ai_frame)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Start Game", font=("Helvetica", 14), width=15, command=start_game).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Return to Home", font=("Helvetica", 14), width=15,
                command=lambda: [ai_frame.destroy(), self.landing_screen()]).pack(side=tk.LEFT, padx=10)


    def start_ai_game(self, difficulty="Easy"):
        self.game = TicTacToe(self.board_size)
        self.ai_difficulty = difficulty

        if self.game_frame:
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True)

        self.status_label = tk.Label(
            self.game_frame,
            text=f"{self.player_names[self.game.current_player]}'s turn ({self.game.current_player})",
            font=("Helvetica", 20), pady=20
        )
        self.status_label.grid(row=0, column=0, columnspan=self.board_size)

        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                btn = tk.Button(self.game_frame, text="", width=8, height=4, font=("Helvetica", 20),
                                command=lambda idx=i * self.board_size + j: self.handle_ai_move(idx))
                btn.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        tk.Button(self.game_frame, text="Return to Home", font=("Helvetica", 14),
                command=lambda: [self.game_frame.destroy(), self.landing_screen()]).grid(
            row=self.board_size + 2, column=0, columnspan=self.board_size, pady=20
        )

        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def handle_ai_move(self, idx):
        if self.game.board[idx] != '_':
            return  # Invalid move

        # Player move
        self.game.make_move(idx)
        row, col = divmod(idx, self.board_size)
        self.buttons[row][col].config(text='X', fg='red')

        if self.game.winner or self.game.is_draw():
            self.ask_reset()
            return

        self.status_label.config(text=f"{self.player_names['O']}'s turn (O)")

        # AI move (basic: random empty spot)
        self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        if self.ai_difficulty == "Hard":
            _, ai_choice = self.minimax(self.game.board, 'O')
        else:
            empty_indices = [i for i, val in enumerate(self.game.board) if val == '_']
            ai_choice = random.choice(empty_indices)

        self.game.make_move(ai_choice)
        row, col = divmod(ai_choice, self.board_size)
        self.buttons[row][col].config(text='O', fg='blue')

        if self.game.winner or self.game.is_draw():
            self.ask_reset()
        else:
            self.status_label.config(text=f"{self.player_names['X']}'s turn (X)")

    def minimax(self, board, player):
        winner = self.check_winner_for_board(board)
        if winner == 'O':
            return (1, None)
        elif winner == 'X':
            return (-1, None)
        elif '_' not in board:
            return (0, None)

        moves = []
        for i in range(len(board)):
            if board[i] == '_':
                new_board = board[:]
                new_board[i] = player
                score, _ = self.minimax(new_board, 'X' if player == 'O' else 'O')
                moves.append((score, i))

        if player == 'O':
            return max(moves)
        else:
            return min(moves)
        
    def check_winner_for_board(self, board):
        size = self.board_size

        # Rows
        for i in range(0, size ** 2, size):
            row = board[i:i + size]
            if row.count(row[0]) == size and row[0] != '_':
                return row[0]

        # Columns
        for col in range(size):
            column = [board[col + row * size] for row in range(size)]
            if column.count(column[0]) == size and column[0] != '_':
                return column[0]

        # Diagonals
        diag1 = [board[i * (size + 1)] for i in range(size)]
        diag2 = [board[(i + 1) * (size - 1)] for i in range(size)]
        if diag1.count(diag1[0]) == size and diag1[0] != '_':
            return diag1[0]
        if diag2.count(diag2[0]) == size and diag2[0] != '_':
            return diag2[0]

        return None

    def start_match_game(self):
        self.game = TicTacToe(self.board_size)

        if self.game_frame:
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True)

        # Round + Score display
        round_info = f"Game {self.current_game} of {self.total_games}"
        score_info = f"{self.player_names['X']}: {self.scores['X']}    {self.player_names['O']}: {self.scores['O']}"
        
        tk.Label(self.game_frame, text=round_info, font=("Helvetica", 16, "bold"), pady=10).grid(
            row=0, column=0, columnspan=self.board_size
        )

        tk.Label(self.game_frame, text=score_info, font=("Helvetica", 14)).grid(
            row=1, column=0, columnspan=self.board_size
        )

        # Status label
        self.status_label = tk.Label(
            self.game_frame,
            text=f"{self.player_names[self.game.current_player]}'s turn ({self.game.current_player})",
            font=("Helvetica", 16), pady=10
        )
        self.status_label.grid(row=2, column=0, columnspan=self.board_size)

        # Buttons
        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                btn = tk.Button(self.game_frame, text="", width=8, height=4, font=("Helvetica", 20),
                                command=lambda idx=i * self.board_size + j: self.handle_match_move(idx))
                btn.grid(row=i + 3, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        # Return to Home Button
        tk.Button(
            self.game_frame,
            text="Return to Home",
            font=("Helvetica", 14),
            command=lambda: [self.game_frame.destroy(), self.landing_screen()]
        ).grid(row=self.board_size + 4, column=0, columnspan=self.board_size, pady=20)

    def start_multiplayer_game(self, player1_name, player2_name):
        self.player_names = {'X': player1_name, 'O': player2_name}
        self.game = TicTacToe(self.board_size)

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True)

        self.status_label = tk.Label(self.game_frame,
                                    text=f"{self.player_names[self.game.current_player]}'s turn ({self.game.current_player})",
                                    font=("Helvetica", 20), pady=20)
        self.status_label.grid(row=0, column=0, columnspan=self.board_size)

        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                btn = tk.Button(self.game_frame, text="", width=8, height=4, font=("Helvetica", 20),
                                command=lambda idx=i * self.board_size + j: self.handle_move(idx))
                btn.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        # Return to Home Button
        tk.Button(
            self.game_frame,
            text="Return to Home",
            font=("Helvetica", 14),
            command=lambda: [self.game_frame.destroy(), self.landing_screen()]
        ).grid(row=self.board_size + 4, column=0, columnspan=self.board_size, pady=20)

    def handle_move(self, idx):
        if self.game.make_move(idx):
            row, col = divmod(idx, self.board_size)
            self.buttons[row][col].config(
                text=self.game.board[idx],
                fg='red' if self.game.board[idx] == 'X' else 'blue'
            )

            if self.game.winner or self.game.is_draw():
                self.ask_reset()
            else:
                self.status_label.config(
                    text=f"{self.player_names[self.game.current_player]}'s turn ({self.game.current_player})"
                )

    def handle_match_move(self, idx):
        if self.game.make_move(idx):
            row, col = divmod(idx, self.board_size)
            self.buttons[row][col].config(
                text=self.game.board[idx],
                fg='red' if self.game.board[idx] == 'X' else 'blue'
            )

            if self.game.winner:
                winner = self.game.winner
                self.scores[winner] += 1
                self.show_match_result(f"{self.player_names[winner]} wins this round!")

            elif self.game.is_draw():
                self.show_match_result("It's a draw!")

            else:
                self.status_label.config(
                    text=f"{self.player_names[self.game.current_player]}'s turn ({self.game.current_player})"
                )

    def show_match_result(self, result_text):
        win_target = (self.total_games // 2) + 1
        if self.scores['X'] >= win_target or self.scores['O'] >= win_target:
            self.show_final_winner()
        elif self.current_game == self.total_games:
            self.show_final_winner()
        else:
            popup = tk.Toplevel(self.root)
            popup.title("Round Over")
            popup.transient(self.root)
            popup.grab_set()

            popup.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))

            tk.Label(popup, text=result_text, font=("Helvetica", 16), pady=10).pack()
            tk.Label(popup, text="Continue to next game?", font=("Helvetica", 14)).pack()
            

            def next_game():
                popup.destroy()    
                self.current_game += 1
                self.start_match_game()

            def quit_match():
                popup.destroy()
                self.game_frame.destroy()
                self.landing_screen()

            
            tk.Button(popup, text="Next Game", font=("Helvetica", 14), width=12, command=next_game).pack(side=tk.LEFT, padx=10, pady=20)
            tk.Button(popup, text="Return to Home", font=("Helvetica", 14), width=15, command=quit_match).pack(side=tk.LEFT, padx=10, pady=20)
        
    def show_final_winner(self):
        popup = tk.Toplevel(self.root)
        popup.title("Match Over")
        popup.transient(self.root)
        popup.grab_set()

        popup.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))

        x_score, o_score = self.scores['X'], self.scores['O']
        if x_score > o_score:
            winner_text = f"{self.player_names['X']} wins the series!"
        elif o_score > x_score:
            winner_text = f"{self.player_names['O']} wins the series!"
        else:
            winner_text = "The series ends in a draw!"

        tk.Label(popup, text=winner_text, font=("Helvetica", 16, "bold"), pady=10).pack()
        tk.Label(popup, text="Would you like to return to the main menu?", font=("Helvetica", 14)).pack()

        def return_home():
            popup.destroy()
            self.game_frame.destroy()
            self.landing_screen()

        tk.Button(popup, text="Return to Home", font=("Helvetica", 14), width=20, command=return_home).pack(pady=20)

    def ask_reset(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.transient(self.root)
        popup.grab_set()  # Makes it modal

        # Center the popup
        popup.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))

        result_text = (
            f"{self.player_names[self.game.winner]} wins!"
            if self.game.winner
            else "It's a draw!"
        )

        tk.Label(popup, text=result_text, font=("Helvetica", 18), pady=10).pack()
        tk.Label(popup, text="Would you like to play again?", font=("Helvetica", 14), pady=10).pack()

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=15)

        def play_again():
            popup.destroy()
            self.game.reset()
            for row in self.buttons:
                for btn in row:
                    btn.config(text="")
            self.status_label.config(
                text=f"{self.player_names[self.game.current_player]}'s turn ({self.game.current_player})"
            )

        def return_home():
            popup.destroy()
            self.game_frame.destroy()
            self.landing_screen()

        tk.Button(btn_frame, text="Yes", font=("Helvetica", 14), width=12, command=play_again).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Return to Home", font=("Helvetica", 14), width=15, command=return_home).pack(side=tk.LEFT, padx=10)

    def run(self):
        self.root.mainloop()
