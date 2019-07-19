import json
import re


class AlphaPuzzleSolver:

    h_word_list = []
    v_word_list = []

    def __init__(self, puzzle, all_words):
        self.puzzle = puzzle
        self.board = puzzle.get("board")
        self.letters = puzzle.get("letters")
        self.all_words = all_words

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

    def solve_board(self):
        while len(self.letters) < 26:
            self.substitutor()
            for partial_word in self.h_word_list:
                self.word_search(partial_word)
            for partial_word in self.v_word_list:
                self.word_search(partial_word)

        self.print_word_lists()

    def substitutor(self):
        for word in self.h_word_list:
            for char in word:
                for num, letter in self.letters.items():
                    if char == num:
                        char = letter
        for word in self.v_word_list:
            for char in word:
                for num, letter in self.letters.items():
                    if char == num:
                        char = letter


    def word_search(self, partial_word):
        # Find pairs of matching characters
        char_pairs = self.find_pairs(partial_word)
        regex = self.create_regex(partial_word)
        # search for all words using regex
        possible_words = self.search_dictionary(regex)
        for word in possible_words:
            for pair in char_pairs:
                if word[pair[0]] != word[pair[1]]:
                    possible_words.remove(word)

        if len(possible_words) == 1:
            self.update_letters(possible_words[0], partial_word)
            # partial_word = list(possible_words[0])

    def find_pairs(self, partial_word):
        char_pairs = []
        for i in range(len(partial_word)):
            j = i + 1
            while j < len(partial_word):
                if partial_word[i] == partial_word[j]:
                    char_pairs.append((i, j))
                j += 1
        return char_pairs

    def create_regex(self, partial_word):
        regex = "^"
        for char in partial_word:
            if char.isalpha():
                regex += char
            else:
                regex += "."
        regex += "$"
        return regex

    def search_dictionary(self, regex):
        matches = []
        for s in self.all_words:
            match = re.search(regex, s)
            if match:
                matches.append(match)
        return matches

    def update_letters(self, complete_word, partial_word):
        for i in range(partial_word):
            if partial_word[i].isdigit():
                new_entry = {partial_word[i]: complete_word[i]}
                self.letters.update(new_entry)

    def print_word_lists(self):
        print(self.h_word_list)
        print(self.v_word_list)
        # print(self.all_words)

if __name__ == "__main__":
    all_words = []
    with open("day1.json", 'r') as f1:
        day_1 = json.load(f1)
    with open("all_words.txt", 'r') as f2:
        for line in f2:
            all_words.append(line)
    solver = AlphaPuzzleSolver(day_1, all_words)
    solver.parse_board()
    solver.solve_board()
