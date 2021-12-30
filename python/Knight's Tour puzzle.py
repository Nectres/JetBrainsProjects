class KnightTour:
    def __init__(self):
        rows, cols = self.get_dimensions("Enter your board dimensions: ", lambda x: x > 0, lambda y: y > 0, decrement=False)
        self.cell_size = len(str(rows * cols))
        self.border = ' ' + '-' * (cols * (self.cell_size + 1) + 3)
        self.rows = rows
        self.empty_cell = self.cell_size * '_'
        self.knight = "X".rjust(self.cell_size, ' ')
        self.possible_move = "O".rjust(self.cell_size, ' ')
        self.board = [
            [self.empty_cell for _ in range(cols)] for _ in range(rows)]
        self.cols = cols
        self.visited_cell = '*'.rjust(self.cell_size, ' ')
        self.visited = 0
        self.knight_pos = (0, 0)

    def print_possible_moves(self):

        moves = self.get_moves_for_knight()

        print(self.border)
        for i in range(self.rows-1, -1, -1):
            print(f'{i+1}| ', end='')
            for j in range(self.cols):
                if (i, j) in moves:
                    possible_moves = self.get_moves_for_knight(i, j)
                    # - 1 to not revisit this position
                    num_of_moves = len(possible_moves) - 1
                    if num_of_moves < 0:
                        num_of_moves = 0
                    print(str(num_of_moves).rjust(self.cell_size, " "), end=" ")
                else:
                    print(self.board[i][j], end=' ')
            print('|')
        print(self.border)
        print('   ', end='')
        for i in range(1, self.cols+1):
            print(str(i).rjust(self.cell_size, ' '), end=' ')
        print()
        return moves

    def move(self, x, y):
        self.visited += 1
        self.board[self.knight_pos[0]][self.knight_pos[1]] = self.visited_cell
        self.board[x][y] = self.knight
        self.knight_pos = (x, y)

    def get_knight_pos(self):
        row, col = self.get_dimensions("Enter the knight's starting position: ",lambda x: 0 <= x < self.rows, lambda y: 0 <= y < self.cols)
        self.board[row][col] = self.knight
        self.knight_pos = (row, col)
        self.visited = 1

    def get_moves_for_knight(self, x=None, y=None):
        if not x:
            x = self.knight_pos[0]
            y = self.knight_pos[1]
        moves = []

        for i in [-1, 1]:
            for j in [2, -2]:
                moves.append((x+i, y+j))

        for i in [-1, 1]:
            for j in [2, -2]:
                moves.append((x+j, y+i))
        legal_moves = tuple(pos for pos in moves if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols and self.board[pos[0]][pos[1]] != self.visited_cell and pos != (x,y))
        return legal_moves

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

    def start(self):
        self.get_knight_pos()
        while True:
            x = 0
            y = 0
            possible_moves = self.print_possible_moves()
            if len(possible_moves) < 1:
                break

            while True:
                x, y = self.get_dimensions("Enter your next move: ",  lambda x: 0 <= x < self.rows,  lambda y: 0 <= y < self.cols)
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


def main():
    game = KnightTour()
    game.start()


if __name__ == '__main__':
    main()
