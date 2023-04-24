import random

class Connect4:
    def __init__(self, rows=6, cols=7, win_length=4):
        self.rows = rows
        self.cols = cols
        self.win_length = win_length
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1
        self.moves = []

    def print_board(self):
        print('  '.join(str(i) for i in range(self.cols)))
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, col):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = str(self.current_player)
                self.moves.append((row, col))
                return True
        return False

    def check_win(self):
        for row, col in self.moves:
            player = self.board[row][col]
            if self.check_row(row, player) or self.check_col(col, player) or self.check_diag(row, col, player):
                return player
        return None

    def check_row(self, row, player):
        for col in range(self.cols - self.win_length + 1):
            if all(self.board[row][col+i] == player for i in range(self.win_length)):
                return True
        return False

    def check_col(self, col, player):
        for row in range(self.rows - self.win_length + 1):
            if all(self.board[row+i][col] == player for i in range(self.win_length)):
                return True
        return False

    def check_diag(self, row, col, player):
        if row >= self.win_length - 1 and col <= self.cols - self.win_length:
            if all(self.board[row-i][col+i] == player for i in range(self.win_length)):
                return True
        if row <= self.rows - self.win_length and col <= self.cols - self.win_length:
            if all(self.board[row+i][col+i] == player for i in range(self.win_length)):
                return True
        if row <= self.rows - self.win_length and col >= self.win_length - 1:
            if all(self.board[row+i][col-i] == player for i in range(self.win_length)):
                return True
        if row >= self.win_length - 1 and col >= self.win_length - 1:
            if all(self.board[row-i][col-i] == player for i in range(self.win_length)):
                return True
        return False

class Connect3(Connect4):
    def __init__(self, rows=6, cols=7):
        super().__init__(rows, cols, win_length=3)

class Connect5(Connect4):
    def __init__(self, rows=6, cols=7):
        super().__init__(rows, cols, win_length=5)

class Connect4Plus(Connect4):
    def __init__(self, rows=6, cols=7, win_length=4):
        super().__init__(rows, cols, win_length)
        self.blocked_row = None
        self.blocked_col = None

    def print_board(self):
        if self.blocked_row is not None and self.blocked_col is not None:
            self.board[self.blocked_row][self.blocked_col] = 'X'
        super().print_board()

    def make_move(self, col):
        if self.blocked_row is None and self.blocked_col is not None:
            if self.blocked_row is None and random.random() < 0.2:
                self.blocked_row = random.randint(0, self.rows - 1)
                self.blocked_col = random.randint(0, self.cols - 1)
            if self.blocked_row is not None and self.blocked_col is not None and col == self.blocked_col:
                return False
            return super().make_move(col)

        class Game:
            def __init__(self):
                self.players = []
                self.game_type = None
                self.win_length = None
                self.high_scores = {}

            def start(self):
                print('Welcome to Connect 4!')
                while True:
                    num_players = input('How many players will be playing? (2 or 3) ')
                    if num_players == '2' or num_players == '3':
                        break
                    else:
                        print('Invalid input, please try again.')
                for i in range(int(num_players)):
                    name = input(f'Player {i + 1}, please enter your name: ')
                    self.players.append(name)
                while True:
                    game_type = input('Select game type: (3, 4, or 5) ')
                    if game_type == '3' or game_type == '4' or game_type == '5':
                        self.game_type = game_type
                        self.win_length = int(game_type)
                        break
                    else:
                        print('Invalid input, please try again.')
                self.play_game()

            def play_game(self):
                if self.game_type == '3':
                    game = Connect3()
                elif self.game_type == '5':
                    game = Connect5()
                else:
                    game = Connect4Plus(win_length=self.win_length)
                game.print_board()
                while True:
                    move = input(
                        f"{self.players[game.current_player - 1]}, please select a column to drop your piece (0-6): ")
                    if move.isdigit() and int(move) >= 0 and int(move) < game.cols:
                        col = int(move)
                        if game.make_move(col):
                            game.print_board()
                            winner = game.check_win()
                            if winner is not None:
                                print(f'Congratulations, {self.players[int(winner) - 1]} wins!')
                                self.update_high_scores(self.players[int(winner) - 1])
                                break
                            elif len(game.moves) == game.rows * game.cols:
                                print('Game over, it is a tie!')
                                break
                            game.current_player = 3 - game.current_player
                        else:
                            print('That column is full, please try again.')
                    else:
                        print('Invalid input, please try again.')

            def update_high_scores(self, player):
                if player not in self.high_scores:
                    self.high_scores[player] = 1
                else:
                    self.high_scores[player] += 1
                with open('high_scores.txt', 'w') as f:
                    for player, score in self.high_scores.items():
                        f.write(f'{player}: {score}\n')
                print('High scores updated.')

            def print_high_scores(self):
                with open('high_scores.txt', 'r') as f:
                    for line in f:
                        print(line.strip())

        if __name__ == 'player1 ; player2':
            game = Game()
            game.start()

