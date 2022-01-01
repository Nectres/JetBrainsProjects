import re


class ProblemStack:
    def __init__(self, line_no: int) -> None:
        self.problems = {}
        self.line_no = line_no

    def add(self, code: str, message: str):
        self.problems[code] = message

    def print(self):
        keys = list(self.problems.keys())
        keys.sort()
        for code in keys:
            msg = self.problems[code]
            print(f'Line {self.line_no}: {code} {msg}')


class Linter:
    def __init__(self, filename) -> None:
        self.filename = filename

    def get_no_of_spaces(self, line: str):
        return (len(line) - len(line.lstrip()))

    def get_comment(self, line: str):
        # remove all strings from the line
        line_without_str = re.sub(r'["\'].*[^\\][\'"]', 'string', line)
        comments = re.search(r'.\s*#', line_without_str, flags=re.IGNORECASE)
        if comments:
            # - 1 because, indices 24 - 23 is not one space but 0
            space_between = comments.end() - comments.start() - 2
            return line_without_str[:comments.start() + 1], line_without_str[comments.end():], space_between
        return line_without_str, '', 0

    def check(self):
        with open(self.filename) as file:
            blank_lines_before_code = 0
            for line_no, line in enumerate(file, 1):
                problems = ProblemStack(line_no)
                if len(line.strip()) == 0:  # blank line
                    blank_lines_before_code += 1
                    continue
                if blank_lines_before_code > 2:
                    problems.add("S006", "More than two blank lines used before this line")
                blank_lines_before_code = 0
                if len(line) > 79:
                    problems.add('S001', 'Too long')
                if self.get_no_of_spaces(line) % 4 != 0:
                    problems.add('S002', 'Indentation is not a multiple of four')
                if line.startswith('#'):
                    plain_line = ''
                    comments = line
                    space_between = 2 # incorrect, but prevents checking
                else:
                    plain_line, comments, space_between = self.get_comment(line)
                # print(line_no, plain_line, space_between, len(comments))
                if plain_line.find(";") != -1:
                    problems.add("S003", 'Unnecessary semicolon')
                if len(comments.strip()) > 0 and space_between < 2:
                    problems.add("S004", "At least two spaces required before inline comments")
                if comments.lower().find("todo") != -1:
                    problems.add("S005", "TODO found")

                problems.print()


def main():
    file_name = input()
    linter = Linter(file_name)
    linter.check()


if __name__ == '__main__':
    main()
