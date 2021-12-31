class Linter:
    def __init__(self, filename) -> None:
        self.filename = filename

    def print(line_no, code, message):
        print(f'Line {line_no}: {code} {message}')

    def check(self):
        with open(self.filename) as file:
            for line_no, line in enumerate(file, 1):
                if len(line) > 79:
                    self.print(line_no, 'S001', 'Too long')

def main():
    file_name = input()
    linter = Linter(file_name)
    linter.check()

if __name__ == '__main__':
    main()
