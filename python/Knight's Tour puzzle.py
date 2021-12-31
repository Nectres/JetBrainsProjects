from typing import Tuple
import sys

sys.setrecursionlimit(10000)

class KnightTour:
    def __init__(self):
        rows, cols = self.get_dimensions(
            "Enter your board dimensions: ", lambda x: x > 0, lambda y: y > 0, decrement=False)
        self.rows = rows
        self.cols = cols
        self.cell_size = len(str(rows * cols))
        self.border = ' ' + '-' * (cols * (self.cell_size + 1) + 3)
        self.empty_cell = self.cell_size * '_'
        self.knight = "X".rjust(self.cell_size, ' ')
        self.visited_cell = '*'.rjust(self.cell_size, ' ')
        self.visited = 1
        self.knight_pos = (0, 0)
        self.board = []
        self.total = self.rows * self.cols
        self.solution_board = []

    def distance_from_center(self, pos: Tuple[int, int]) -> int:
        half_x = self.rows / 2
        half_y = self.cols / 2
        return pow(pow(pos[0] - half_x, 2) + pow(pos[1] - half_y, 2), 0.5)

    def reset_board(self):
        self.board = [[self.empty_cell for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = 1

    def print_possible_moves(self):
        moves = self.get_moves_for_knight()
        print(self.border)
        for i in range(self.rows-1, -1, -1):
            print(f'{i+1}| ', end='')
            for j in range(self.cols):
                if (i, j) in moves:
                    possible_moves = self.get_moves_for_knight(i, j)
                    # - 1 to not revisit this position
                    num_of_moves = len(possible_moves)
                    if num_of_moves < 0:
                        num_of_moves = 0
                    print(str(num_of_moves).rjust(
                        self.cell_size, " "), end=" ")
                else:
                    print(self.board[i][j], end=' ')
            print('|')
        print(self.border)
        print('   ', end='')
        for i in range(1, self.cols+1):
            print(str(i).rjust(self.cell_size, ' '), end=' ')
        print()
        return moves

    def move(self, x, y, fill_with=None):
        if not fill_with:
            fill_with = self.knight
            self.board[self.knight_pos[0]
                       ][self.knight_pos[1]] = self.visited_cell
        self.board[x][y] = fill_with
        self.visited += 1
        self.knight_pos = (x, y)

    def get_knight_pos(self):
        row, col = self.get_dimensions(
            "Enter the knight's starting position: ", lambda x: 0 <= x < self.rows, lambda y: 0 <= y < self.cols)
        self.reset_board()
        self.knight_pos = (row, col)

    def get_moves_for_knight(self, x=None, y=None) -> Tuple[Tuple[int, int]]:
        if not x:
            x, y = self.knight_pos
        moves = []
        for i in [-1, 1]:
            for j in [2, -2]:
                moves.append((x+i, y+j))
        for i in [-1, 1]:
            for j in [2, -2]:
                moves.append((x+j, y+i))
        legal_moves = tuple(pos for pos in moves if 0 <= pos[0] < self.rows and 0 <= pos[1]
                            < self.cols and self.board[pos[0]][pos[1]] == self.empty_cell and pos != (x, y))
        return legal_moves

    def print_board(self):
        print(self.border)
        for i in range(self.rows-1, -1, -1):
            print(f'{i+1}| ', end='')
            for j in range(self.cols):
                cell = self.board[i][j]
                print(str(cell).rjust(self.cell_size), end=' ')
            print('|')
        print(self.border)
        print('   ', end='')
        for i in range(1, self.cols+1):
            print(str(i).rjust(self.cell_size, ' '), end=' ')
        print()

    def get_dimensions(self, prompt: str, check_x, check_y, decrement=True):
        valid = False
        x = 0
        y = 0
        while not valid:
            string = input(prompt)
            try:
                coordinates = [int(x) for x in string.split()]
            except ValueError:
                print("Invalid dimensions!")
                continue
            if len(coordinates) != 2:
                print("Invalid dimensions!")
                continue
            y, x = coordinates
            if decrement:
                x -= 1
                y -= 1
            if not check_x(x) or not check_y(y):
                print("Invalid dimensions!")
                continue
            # If all checks have passed, the position is valid, and so we can break the loop
            valid = True
        return x, y
    
    def is_board_solved(self):
        return all([row.count(self.empty_cell) == 0 for row in self.board])

    def get_next_moves(self, board, row, col):
        moves = []
        for i in [-1, 1]:
            for j in [2, -2]:
                moves.append((row+i, col+j))
        for i in [-1, 1]:
            for j in [2, -2]:
                moves.append((row+j, col+i))
        legal = [pos for pos in moves if 0 <= pos[0] < self.rows and 0 <=
                pos[1] < self.cols and board[pos[0]][pos[1]] == 0]
        return legal

    def check_for_solution(self,board,x,y, counter):
        board[x][y] = counter
        if counter == self.total:
            return board
        possible_moves = self.get_next_moves(board,x,y)
        if len(possible_moves) < 1:
            return
        accesibility_map = {pos:len(self.get_next_moves(board,pos[0], pos[1])) for pos in possible_moves}
        least = min(accesibility_map.values())
        next_moves = [pos for pos, accessibility in accesibility_map.items() if accessibility == least]
        for move in next_moves:
            stack = self.check_for_solution(board, move[0], move[1], counter+1)
            if stack is not None:
                return stack
        return
    
    def get_solution(self):
        zero_board =  [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        row,col = self.knight_pos
        stack = self.check_for_solution(zero_board, row, col, 1)
        if stack is not None:
            self.solution_board = stack
            return True
        else:
            return False 


    def start(self):
        self.get_knight_pos()
        while True:
            menu_choice = input("Do you want to try the puzzle? (y/n): ")
            if menu_choice not in ('n', 'y'):
                print("Invalid input!")
                continue
            break
        # creates self.solution_board if solution exists
        solution_exists = self.get_solution()
        if not solution_exists:
            print("No solution exists!")
            return
        if menu_choice == 'y':
            row, col = self.knight_pos
            self.board[row][col] = self.knight
            while True:
                possible_moves = self.print_possible_moves()
                if len(possible_moves) < 1:
                    break
                while True:
                    x, y = self.get_dimensions("Enter your next move: ", lambda x: 0 <= x < self.rows, lambda y: 0 <= y < self.cols)
                    if (x, y) not in possible_moves:
                        print("Invalid move! ", end="")
                        continue
                    break
                self.move(x, y)
            if self.visited == self.rows * self.cols:
                print("What a great tour! Congratulations!")
            else:
                print(
                    f"No more possible moves!\nYour knight visited {self.visited} squares!")
        elif solution_exists:  # player has chosen 'n'
            self.board = self.solution_board
            print("\nHere's the solution!")
            self.print_board()


def main():
    game = KnightTour()
    game.start()


if __name__ == '__main__':
    main()
