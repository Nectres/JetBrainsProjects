class KnightTour:
    def __init__(self):
        cols, rows = self.get_dimensions(
            "Enter your board dimensions: ", lambda x: x > 0, decrement=False)
        self.cell_size = len(str(rows * cols))
        self.border = ' ' + '-' * (cols * (self.cell_size + 1) + 3)
        self.rows = rows
        self.empty_cell = self.cell_size * '_'
        self.knight = "X".rjust(self.cell_size, ' ')
        self.board = [
            [self.empty_cell for _ in range(cols)] for _ in range(rows)]
        self.cols = cols
        self.get_knight_pos()

    def print_board(self):
        print(self.border)
        for i in range(self.rows-1, -1, -1):
            print(f'{i+1}| ', end='')
            for j in range(self.cols):
                print(self.board[i][j], end=' ')
            print('|')
        print(self.border)
        print('   ', end='')
        for i in range(1, self.cols+1):
            print(str(i).rjust(self.cell_size,' '), end=' ')

    def get_knight_pos(self):
        col, row = self.get_dimensions("Enter the knight's starting position: ", lambda x: 0 <= x <= self.cols-1, lambda y: 0 <= y <= self.rows-1)
        self.board[row][col] = self.knight

    def get_dimensions(self, prompt: str, check_x, check_y=None, decrement=True):
        valid = False
        if not check_y:
            check_y = check_x
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

            x, y = coordinates

            if decrement:
                x -= 1
                y -= 1

            if not check_x(x) or not check_y(y):
                print("Invalid dimensions!")
                continue

            # If all checks have passed, the position is valid and we can break the loop
            valid = True
        return x, y


def main():
    game = KnightTour()
    game.print_board()


if __name__ == '__main__':
    main()
