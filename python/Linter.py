import re
from typing import Dict
import os.path as path
import os
import sys


class ProblemStack:
    def __init__(self, fullpath: str) -> None:
        self.path = fullpath
        self.line_no = 1
        self.problems = {1: {}}

    def next_line(self):
        self.line_no += 1
        self.problems[self.line_no] = {}

    def add(self, code: str, message: str):
        self.problems[self.line_no][code] = message

    def print(self):
        lines = list(self.problems.keys())
        lines.sort()
        for line in lines:
            codes = list(self.problems[line].keys())
            codes.sort()
            for code in codes:
                msg = self.problems[line][code]
                print(f'{self.path}: Line {line}: {code} {msg}')


class Linter:

    def __init__(self, fullpath: str) -> None:
        self.path = fullpath
        if path.isdir(fullpath):
            files = os.listdir(fullpath)
            self.multiple = True
            self.files = files
        elif path.isfile(fullpath):
            self.multiple = False

    def get_no_of_spaces(self, line: str):
        return len(line) - len(line.lstrip())

    def get_comment(self, line: str):
        # remove all strings from the line
        line_without_str = re.sub(r'["\'].*[^\\][\'"]', 'string', line)
        comments = re.search(r'.\s*#', line_without_str, flags=re.IGNORECASE)
        if comments:
            # - 1 because, indices 24 - 23 is not one space but 0
            space_between = comments.end() - comments.start() - 2
            return line_without_str[:comments.start() + 1], line_without_str[comments.end():], space_between
        return line_without_str, '', 0

    def check(self, fullpath):
        with open(fullpath) as file:
            blank_lines_before_code = 0
            problems = ProblemStack(fullpath)
            for line in file:
                if len(line.strip()) == 0:  # blank line
                    blank_lines_before_code += 1
                    problems.next_line()
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
                    space_between = 2  # incorrect, but prevents checking
                else:
                    plain_line, comments, space_between = self.get_comment(
                        line)
                # print(line_no, plain_line, space_between, len(comments))
                if plain_line.find(";") != -1:
                    problems.add("S003", 'Unnecessary semicolon')
                if len(comments.strip()) > 0 and space_between < 2:
                    problems.add(
                        "S004", "At least two spaces required before inline comments")
                if comments.lower().find("todo") != -1:
                    problems.add("S005", "TODO found")
                problems.next_line()
            return problems

    def start(self):
        if not self.multiple:
            stack = self.check(self.path)
            stack.print()
        else:
            stacks: Dict[str, ProblemStack] = {}
            python_files = [file for file in self.files if file.endswith('.py')]
            for file in python_files:
                fullpath = path.join(self.path, file)
                stacks[file] = self.check(fullpath)
            python_files.sort()
            for file in python_files:
                stacks[file].print()


def main():
    linter = Linter(sys.argv[1])
    linter.start()


if __name__ == '__main__':
    main()
