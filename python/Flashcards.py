import io
import json
import random
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('--export_to', help="Specify a file to which to write all the cards entered during execution")
parser.add_argument('--import_from', help="Specify a file name to import the cards from")

args = parser.parse_args()


def find_all_indices(mylist: list, elem):
    indices = []
    prev = 0
    for _ in range(mylist.count(elem)):
        index = mylist[prev:].index(elem)
        indices.append(index + prev)
        prev = index + 1
    return indices


class CardStore:

    def __init__(self) -> None:
        self.log_mem = io.StringIO()
        self.terms: list[str] = []
        self.answers: list[str] = []
        self.mistakes: list[int] = []

    def random_card_index(self):
        return random.randint(0, len(self.terms)-1)

    def save_log(self):
        filename = self.input("File name:")
        with open(filename, 'w') as log_file:
            self.log_mem.seek(0)
            logs = self.log_mem.read()
            pos = len(logs)
            log_file.write(logs)
            self.log_mem.seek(pos)
            self.print("The log has been saved")

    def export(self, filename):
        with open(filename, 'w') as export_file:
            total = len(self.terms)
            dump = json.dumps(
                {'terms': self.terms, 'answers': self.answers, 'mistakes': self.mistakes})
            export_file.write(dump)
            self.print(f'{total} cards have been saved')

    def import_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                card_store_dump = file.read()
                file_card_store = json.loads(card_store_dump)
                self.terms = file_card_store['terms']
                self.answers = file_card_store['answers']
                self.mistakes = file_card_store['mistakes']
                total_cards = len(self.terms)
                self.print(f'{total_cards} cards have been loaded.')
        except OSError:
            self.print("File not found.")

    def print(self, string):
        print(string, file=self.log_mem)
        print(string)

    def input(self, string) -> str:
        prompt = string + '\n'
        result = input(prompt)
        print(prompt, result, file=self.log_mem)
        return result

    def ask(self, num):
        for _ in range(num):
            index = self.random_card_index()
            term = self.terms[index]
            answer = self.answers[index]
            res = self.input('Print the definition of "%s":' % term)
            if res == answer:
                self.print("Correct!")
            elif res in self.answers:
                self.mistakes[index] += 1
                correct_index = self.answers.index(res)
                correct_term = self.terms[correct_index]
                self.print(
                    f'Wrong. The right answer is "{answer}", but your definition is correct for "{correct_term}" card.')
            else:
                self.mistakes[index] += 1
                self.print(f'Wrong. The right answer is "{answer}"')

    def add(self):
        term = self.input("The card:")

        while term in self.terms:
            term = self.input(f'The card "{term}" already exists. Try again:')

        definition = self.input("The definition of the card:")

        while definition in self.answers:
            definition = self.input(
                f'The definition "{definition}" already exists. Try again:')

        self.terms.append(term)
        self.answers.append(definition)
        self.mistakes.append(0)

        self.print(f'The pair ("{term}":"{definition}") has been added.')

    def remove(self):
        term = self.input("Which card?")
        if term not in self.terms:
            self.print(f'Can\'t remove "{term}": there is no such card.')
            return
        index = self.terms.index(term)
        self.answers = self.answers[:index] + self.answers[index+1:]
        self.terms = self.terms[:index] + self.terms[index+1:]
        self.mistakes = self.mistakes[:index] + self.mistakes[index+1:]
        self.print("The card has been removed")

    def hardest_card(self):
        if len(self.mistakes) == 0:
            self.print('There are no cards with errors.')
            return
        hardest = max(self.mistakes)
        if hardest == 0:
            self.print('There are no cards with errors.')
            return
        hardest_indices = find_all_indices(self.mistakes, hardest)
        if len(hardest_indices) == 1:
            index = hardest_indices[0]
            term = self.terms[index]
            self.print(
                f'The hardest card is "{term}". You have {hardest} errors answering it.')
        else:
            string = 'The hardest cards are ' + \
                ", ".join([f'"{self.terms[index]}"' for index in hardest_indices]
                          ) + f'. You have {hardest} errors answering them.'
            self.print(string)

    def start(self):
        if args.import_from:
            self.import_from_file(args.import_from)

        while True:
            menu_choice = self.input(
                "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")

            if menu_choice == 'exit':
                print("bye bye")
                if args.export_to:
                    self.export(args.export_to)
                break
            elif menu_choice == 'add':
                self.add()
            elif menu_choice == 'remove':
                self.remove()
            elif menu_choice == 'export':
                filename = self.input("File name:")
                self.export(filename)
            elif menu_choice == 'import':
                filename = self.input("File name:")
                self.import_from_file(filename)
            elif menu_choice == 'log':
                self.save_log()
            elif menu_choice == 'ask':
                num = int(self.input("How many times to ask?"))
                self.ask(num)
            elif menu_choice == 'hardest card':
                self.hardest_card()
            elif menu_choice == 'reset stats':
                self.mistakes = [0 for _ in self.terms]
                self.print('Card statistics have been reset.')


def main():
    game = CardStore()
    game.start()


if __name__ == '__main__':
    main()
