import random
from collections import Counter

class TicTacToeBoard:
    def _init_(self):
        # Initialize an empty Tic-Tac-Toe board
        self.cells = [' '] * 9

    def _str_(self):
        # Display the board in a readable format with some decorations
        return (
            "\n   0   |   1   |   2      %s   |   %s   |   %s\n"
            "-------+-------+-------   -------+-------+-------\n"
            "   3   |   4   |   5      %s   |   %s   |   %s\n"
            "-------+-------+-------   -------+-------+-------\n"
            "   6   |   7   |   8      %s   |   %s   |   %s\n"
        ) % tuple(self.cells)

    def is_move_valid(self, move):
        # Check if the player's move is valid
        if move.isdigit() and 0 <= int(move) < 9 and self.cells[int(move)] == ' ':
            return True
        return False

    def check_winner(self):
        # Check all winning combinations on the board
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for a, b, c in winning_combinations:
            if self.cells[a] == self.cells[b] == self.cells[c] != ' ':
                return True
        return False

    def is_draw(self):
        # Check if the game is a draw
        return all(cell != ' ' for cell in self.cells)

    def make_move(self, position, marker):
        # Mark the board at the specified position
        self.cells[position] = marker

    def board_state(self):
        # Convert the board to a string representation
        return ''.join(self.cells)


class LearningPlayer:
    def _init_(self):
        # Initialize the player with a dictionary for moves
        self.move_memory = {}
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def start_new_game(self):
        # Start a new game by resetting moves played
        self.moves_in_game = []

    def choose_move(self, game_board):
        # Get a move from the board
        board_representation = game_board.board_state()
        if board_representation not in self.move_memory:
            # If board state is new, initialize it with potential moves
            potential_moves = [i for i, cell in enumerate(board_representation) if cell == ' ']
            self.move_memory[board_representation] = potential_moves * ((len(potential_moves) + 2) // 2)

        available_moves = self.move_memory[board_representation]
        if available_moves:
            selected_move = random.choice(available_moves)  # Choose a random available move
            self.moves_in_game.append((board_representation, selected_move))
        else:
            selected_move = -1  # Resign if no moves available
        return selected_move

    def record_win(self):
        # Update move memory for a win
        for board_state, move in self.moves_in_game:
            self.move_memory[board_state].extend([move] * 3)  # Add three beads for the winning path
        self.wins += 1

    def record_draw(self):
        # Update move memory for a draw
        for board_state, move in self.moves_in_game:
            self.move_memory[board_state].append(move)  # Add one bead for draw
        self.draws += 1

    def record_loss(self):
        # Update move memory for a loss
        for board_state, move in self.moves_in_game:
            if move in self.move_memory[board_state]:
                self.move_memory[board_state].remove(move)  # Remove a bead for the losing path
        self.losses += 1

    def display_statistics(self):
        # Print statistics of the player
        print(f'Learned {len(self.move_memory)} unique board states.')
        print(f'Wins/Draws/Losses: {self.wins}/{self.draws}/{self.losses}')

    def display_probabilities(self, game_board):
        # Display the move statistics for the current board
        board_representation = game_board.board_state()
        try:
            print("Move probabilities for this board: " +
                  str(Counter(self.move_memory[board_representation]).most_common()))
        except KeyError:
            print("This board state has never been seen before.")


class HumanOpponent:
    def _init_(self):
        pass

    def start_new_game(self):
        print("Let's start the game!")

    def choose_move(self, game_board):
        # Ask the human player for a move
        while True:
            move = input('Please enter your move (0-8): ')
            if game_board.is_move_valid(move):
                return int(move)  # Return the valid move
            print("Invalid move. Try again.")

    def record_win(self):
        print("Congratulations, you won!")

    def record_draw(self):
        print("The game ended in a draw.")

    def record_loss(self):
        print("You lost. Better luck next time!")

    def display_probabilities(self, game_board):
        pass  # No statistics to print for human player


def play_tic_tac_toe(player_one, player_two, silent_mode=False):
    # Main game loop
    player_one.start_new_game()
    player_two.start_new_game()
    game_board = TicTacToeBoard()

    if not silent_mode:
        print("\nStarting a new game of Tic-Tac-Toe!")
        print(game_board)

    while True:
        if not silent_mode:
            player_one.display_probabilities(game_board)
        move = player_one.choose_move(game_board)  # Player one's turn
        if move == -1:
            if not silent_mode:
                print("Player resigns!")
            player_one.record_loss()
            player_two.record_win()
            break

        game_board.make_move(move, 'X')  # Player one plays 'X'
        if not silent_mode:
            print(game_board)
        if game_board.check_winner():
            player_one.record_win()
            player_two.record_loss()
            break
        if game_board.is_draw():
            player_one.record_draw()
            player_two.record_draw()
            break

        if not silent_mode:
            player_two.display_probabilities(game_board)
        move = player_two.choose_move(game_board)  # Player two's turn
        if move == -1:
            if not silent_mode:
                print("Player resigns!")
            player_two.record_loss()
            player_one.record_win()
            break

        game_board.make_move(move, 'O')  # Player two plays 'O'
        if not silent_mode:
            print(game_board)
        if game_board.check_winner():
            player_two.record_win()
            player_one.record_loss()
            break


if _name_ == '_main_':
    # Main execution starts here
    first_player_menace = LearningPlayer()
    second_player_menace = LearningPlayer()
    human_player = HumanOpponent()

    # Simulate 1000 games between two Learning players
    for _ in range(1000):
        play_tic_tac_toe(first_player_menace, second_player_menace, silent_mode=True)

    # Print statistics for both Learning players
    first_player_menace.display_statistics()
    second_player_menace.display_statistics()

    # Play a game between one Learning player and a human
    play_tic_tac_toe(first_player_menace, human_player)
    play_tic_tac_toe(human_player, second_player_menace)