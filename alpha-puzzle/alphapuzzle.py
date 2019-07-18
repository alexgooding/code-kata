import json


class AlphaPuzzleSolver:

    h_word_list = []
    v_word_list = []

    def __init__(self, puzzle, dictionary):
        self.puzzle = puzzle
        self.board = puzzle.get("board")
        self.dictionary = dictionary

    def parse_board(self):
        word = []
        # Form horizontal words
        for row in self.board:
            for index in row:
                if index == 0 and len(word) > 1:
                    self.h_word_list.append(word)
                    word = []
                elif index == 0 and len(word) < 2:
                    word = []
                elif not index == 0:
                    word.append(str(index))
            if len(word) > 1:
                self.h_word_list.append(word)
                word = []
            elif len(word) < 2:
                word = []

        word = []

        # Form vertical words
        for column in range(len(self.board[0])):
            for index in range(len(self.board)):
                if self.board[index][column] == 0 and len(word) > 1:
                    self.v_word_list.append(word)
                    word = []
                elif self.board[index][column] == 0 and len(word) < 2:
                    word = []
                elif not self.board[index][column] == 0:
                    word.append(str(self.board[index][column]))
            if len(word) > 1:
                self.v_word_list.append(word)
                word = []
            elif len(word) < 2:
                word = []
    #
    # def substitutor(self, puzzle):
    #     for num in puzzle.get("letters"):
    #         for

    def word_search(self, partial_word):
        possible_words = []
        regex = self.create_regex(partial_word)
        # search for all words using regex
        possible_words = self.search_dictionary(partial_word, regex)


    def create_regex(self, partial_word):
        regex = "^"
        for char in partial_word:
            if char.isalpha():
                regex += char
            else:
                regex += "."
        regex += "$"
        return regex

    def search_dictionary(self, partial_word, regex):
        matches = []
        return matches

    def print_word_lists(self):
        print(self.h_word_list)
        print(self.v_word_list)

if __name__ == "__main__":
    with open("day1.json", 'r') as f:
        day_1 = json.load(f)
    solver = AlphaPuzzleSolver(day_1)
    solver.parse_board()
    solver.print_word_lists()
