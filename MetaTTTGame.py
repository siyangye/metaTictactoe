# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable.

from numpy import random

# Base class
class Player():
    def move(self, board):
        pass

    def is_bot(self):
        pass

# Extended class for human player
class HumanPlayer(Player):
    def move(self, board):
        # Specifies the row and column index of the cell to move in
        row = int(input()) - 1;
        col = int(input()) - 1;
        # Check if it's a valid move
        while 0 > row or 8 < row or 0 > col or 8 < col or None != board[int(row / 3)][int(col / 3)][row % 3][col % 3]:
            print ("Invalid move!")
            row = int(input()) - 1;
            col = int(input()) - 1;

        # Update the game board
        board[int(row / 3)][int(col / 3)][row % 3][col % 3] = self
        return int(row / 3), int(col / 3)

    def is_bot(self):
        return False

# Extended class for bot player
class BotPlayer(Player):
    # Bot is a dummy player, it never try to win, but just follow the basic rule
    def move(self, board):
        while True:
            # Find a random cell to move in
            rnd = random.randint(80)
            row = int(rnd / 9)
            col = int(rnd % 9)
            # Check validity
            if None == board[int(row / 3)][int(col / 3)][row % 3][col % 3]:
                break

        board[int(row / 3)][int(col / 3)][row % 3][col % 3] = self
        return int(row / 3), int(col / 3)

    def is_bot(self):
        return True

class Game:
    def __init__(self, O_player, X_player):
        self.board = [
            [[[None, None, None], [None, None, None], [None, None, None]],
            [[None, None, None], [None, None, None], [None, None, None]],
            [[None, None, None], [None, None, None], [None, None, None]]],
            [[[None, None, None], [None, None, None], [None, None, None]],
            [[None, None, None], [None, None, None], [None, None, None]],
            [[None, None, None], [None, None, None], [None, None, None]]],
            [[[None, None, None], [None, None, None], [None, None, None]],
            [[None, None, None], [None, None, None], [None, None, None]],
            [[None, None, None], [None, None, None], [None, None, None]]]
        ]

        self.meta_board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

        self.O_player = O_player
        self.X_player = X_player
        self.current_player = O_player

    def reset_board(self, board):
        for row in board:
            for player in row:
                player = None

    def show_whole_board(self):
        for row in self.board:
            for j in range(3):
                for board in row:
                    for player in board[j]:
                        if self.O_player == player:
                            print('O', end = '')
                        elif self.X_player == player:
                            print('X', end = '')
                        else:
                            # It's an empty cell
                            print('_', end = '')
                    print(' ', end = '')
                print()
            print()

    # For debug only
    def show_board(self, board):
        for row in board:
            for player in row:
                if self.O_player == player:
                    print('O', end = '')
                elif self.X_player == player:
                    print('X', end = '')
                else:
                    print('_', end = '')
            print()

    def show_whole_board_2(self):
        for i in range(3):
            for j in range(3):
                print(i + 1, j + 1, sep = ' ')
                self.show_board(self.board[i][j])

    def check_line(self, first, second, third):
        if None == first:
            if None == second or None == third or second == third:
                return "continue"
            return "draw"
    
        if first == second and first == third:
            return "succeed"
    
        if first != second and None != second or first != third and None != third:
            return "draw"
        return "continue"
    
    def check_matrix(self, matrix):
        result = "draw"
    
        # Check 3 "horizonal" lines
        for row in matrix:
            line_result = self.check_line(row[0], row[1], row[2])
            if "succeed" == line_result:
                return "succeed", row[0]
    
            if "continue" == line_result:
                result = "continue"
    
        # Check 3 "vertical" lines
        for col in range(3):
            line_result = self.check_line(matrix[0][col], matrix[1][col], matrix[2][col])
            if "succeed" == line_result:
                return "succeed", matrix[0][col]
    
            if "continue" == line_result:
                result = "continue"
    
        # Check 2 "diagonal" lines
        line_result = self.check_line(matrix[0][0], matrix[1][1], matrix[2][2])
        if "succeed" == line_result:
            return "succeed", matrix[0][0]
    
        if "continue" == line_result:
            result = "continue"
    
        line_result = self.check_line(matrix[0][2], matrix[1][1], matrix[2][0])
        if "succeed" == line_result:
            return "succeed", matrix[0][2]
    
        if "continue" == line_result:
            result = "continue"
    
        return result, None

    def run(self):
        result = "continue"
        winner = None

        while "continue" == result:
            # If it's a human player, the show the game board and a prompt
            if not self.current_player.is_bot():
                self.show_whole_board()
                #self.show_whole_board_2()
                print("Take ur turn!")
            row, col = self.current_player.move(self.board)
            # Switch turn
            if self.current_player == self.O_player:
                self.current_player = self.X_player
            else:
                self.current_player = self.O_player

            # Check result
            result, winner = self.check_matrix(self.board[row][col])
            if "draw" == result:
                self.reset_board(self.board[row][col])
                result = "continue"

            if "succeed" == result:
                """For debug
                self.show_board(self.board[row][col])
                if self.O_player == winner:
                    print("O wins in board[", row, "][", col , "]", sep = '')
                else:
                    print("X wins in board[", row, "][", col , "]")
                """

                self.meta_board[row][col] = winner
                result, winner = self.check_matrix(self.meta_board)

        # Game over. Show the final game board and the winner or 'draw'
        #self.show_whole_board()
        #self.show_whole_board_2()
        #self.show_board(self.meta_board)
        if self.O_player == winner:
            print("O wins!")
        elif self.X_player == winner:
            print("X wins!")
        else:
            print("It draws.")

if __name__ == '__main__':
    print("Play with a bot?")
    answer = input()
    if 'y' == answer or 'Y' == answer:
        # Play with bot
        print("Play first?")
        answer = input()
        if 'y' == answer or 'Y' == answer:
            # U play first
            game = Game(HumanPlayer(), BotPlayer())
        else:
            # Bot plays first
            game = Game(BotPlayer(), HumanPlayer())
    else:
        # It's a human x human game
        game = Game(HumanPlayer(), HumanPlayer())

    # Game starts!
    game.run()
