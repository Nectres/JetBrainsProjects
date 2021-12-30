class KnightTour:
    def __init__(self, x, y):
        # Generating a 8x8 board with empty ('_') places
        self.board = [['_' for _ in range(8)] for _ in range(8)]
        # Placing the knight in the board at the given position
        self.board[x][y] = 'X'

    def print_board(self):
        print(' -------------------')
        for i in range(7, -1, -1):
            print(f'{i+1}| ', end='')
            for j in range(8):
                print(self.board[i][j], end=' ')
            print('|')
        print(' -------------------')
        print('   1 2 3 4 5 6 7 8 ')


def main():
    string = input("Enter the knight's starting position: ")
    try:
        coordinates = [int(x) - 1 for x in string.split()]
    except ValueError:
        print("Invalid dimensions!")
        return
    if len(coordinates) != 2:
        print("Invalid dimensions!")
        return
    y, x = coordinates
    if not 0 <= x <= 7 or not 0 <= y <= 7:
        print("Invalid dimensions!")
        return
    game = KnightTour(x, y)
    game.print_board()


if __name__ == '__main__':
    main()
