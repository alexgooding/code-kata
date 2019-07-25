import json
import re
import copy
import string


class AlphaPuzzleSolver:

    """
    General workflow:
    1. Parse the board to create two word lists
    2. Substitute the letters we know into the word lists
    3. Find all possible words using a regex search and elimination of words without character pairs
    4. Sort the list of lists of all possible words by length of how many matches there were
    5. create a hypothesis (word guess) using a word from the shortest list of possible words
    6. Substitute these letters into the word lists
    7. Find all possible words
    8. Repeat steps 6 and 7 until we have decrypted the cypher or cannot find any possible words for one word
    9. If we cannot find any possible words, start from scratch but using the next word in the shortest list of possible words as a hypothesis
    """

    h_word_list = []
    v_word_list = []
    h_word_list_original = []
    v_word_list_original = []
    not_found = list(string.ascii_lowercase)

    def __init__(self, puzzle_file_path, all_words_file_path):
        self.all_words = []
        with open(puzzle_file_path, 'r') as f1:
            self.puzzle = json.load(f1)
        with open(all_words_file_path, 'r') as f2:
            for line in f2:
                self.all_words.append(line.lower())
        self.board = self.puzzle.get("board")
        self.letters = dict((k, v.lower()) for k, v in self.puzzle.get("letters").items())
        for char in self.letters.values():
            self.not_found.remove(char.lower())

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

        self.h_word_list_original = copy.deepcopy(self.h_word_list)
        self.v_word_list_original = copy.deepcopy(self.v_word_list)

    def solve_board(self):
        self.substitutor()
        h_possible_words = self.find_all_possible_words(self.h_word_list)
        v_possible_words = self.find_all_possible_words(self.v_word_list)
        h_possible_words.sort(key=len)
        v_possible_words.sort(key=len)
        while True:
            if len(h_possible_words[0]) == 1:
                del h_possible_words[0]
            if len(v_possible_words[0]) == 1:
                del v_possible_words[0]
            if len(h_possible_words[0]) <= len(v_possible_words[0]):
                word_guess = h_possible_words[0][1]
                self.update_letters(word_guess, self.h_word_list[int(h_possible_words[0][0])])
            else:
                word_guess = v_possible_words[0][1]
                self.update_letters(word_guess, self.v_word_list[int(v_possible_words[0][0])])
            print("Assuming word '" + word_guess + "' is correct")
            h_match_flag = True
            v_match_flag = True
            letters_found = 0
            while h_match_flag or v_match_flag:
                self.substitutor()
                # Remove new found letters before forming regex
                for char in self.letters.values():
                    if char.lower() in self.not_found:
                        self.not_found.remove(char.lower())
                h_match_flag = self.find_all_possible_words(self.h_word_list)
                v_match_flag = self.find_all_possible_words(self.v_word_list)

                # TODO Why does it get stuck in a loop when it doesn't find a single possible word (day2 and day3.json)?
                # TODO Need to recursively guess words.
                print("h_match_flag: " + str(h_match_flag))
                print("v_match_flag: " + str(v_match_flag))

                # This may not be the best way.
                if letters_found == len(self.letters):
                    h_match_flag = False
                    v_match_flag = False

                letters_found = len(self.letters)
                print("Number of letters found: " + str(letters_found))


            if len(self.letters) == 26:
                self.create_solution()
                self.print_solution()
                return
            if len(h_possible_words[0]) <= len(v_possible_words[0]):
                del h_possible_words[0][1]
            else:
                del v_possible_words[0][1]
            # Reset the puzzle before starting with new hypothesis
            self.board = copy.deepcopy(self.puzzle.get("board"))
            self.letters = copy.deepcopy(self.puzzle.get("letters"))
            # print(self.letters)
            self.h_word_list = copy.deepcopy(self.h_word_list_original)
            self.v_word_list = copy.deepcopy(self.v_word_list_original)
            self.substitutor()

    def find_all_possible_words(self, word_list):
        all_possible_words = []
        for index, partial_word in enumerate(word_list):
            possible_words = self.word_search(str(index), partial_word)
            if possible_words:
                all_possible_words.append(possible_words)
        return all_possible_words

    def substitutor(self):
        for word_index in range(len(self.h_word_list)):
            for char_index in range(len(self.h_word_list[word_index])):
                for num, letter in self.letters.items():
                    if self.h_word_list[word_index][char_index] == num:
                        self.h_word_list[word_index][char_index] = letter.lower()
        for word_index in range(len(self.v_word_list)):
            for char_index in range(len(self.v_word_list[word_index])):
                for num, letter in self.letters.items():
                    if self.v_word_list[word_index][char_index] == num:
                        self.v_word_list[word_index][char_index] = letter.lower()


    def word_search(self, index, partial_word):
        # Find pairs of matching characters
        char_pairs = self.find_pairs(partial_word)
        regex = self.create_regex(partial_word)
        # search for all words using regex
        possible_words = self.search_dictionary(regex)
        for word in possible_words[:]:
            for pair in char_pairs:
                if word[pair[0]] != word[pair[1]]:
                    possible_words.remove(word)
                    break

        if len(possible_words) == 1:
            self.update_letters(possible_words[0], partial_word)
            return possible_words.insert(0, index)
        elif len(possible_words) == 0:
            return possible_words
        else:
            possible_words.insert(0, index)
            return possible_words

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
                regex += "[" + ",".join(self.not_found) + "]"
        regex += "$"
        return regex

    def search_dictionary(self, regex):
        matches = []
        for s in self.all_words:
            match = re.search(regex, s, re.IGNORECASE)
            if match:
                matches.append(match.group(0))
        return matches

    def update_letters(self, complete_word, partial_word):
        found_letters = self.letters.values()
        for i in range(len(partial_word)):
            if partial_word[i].isdigit():
                new_entry = {partial_word[i]: complete_word[i]}
                self.letters.update(new_entry)
                if complete_word[i] not in found_letters:
                    self.not_found.remove(complete_word[i])
                    found_letters.append(complete_word[i])

    def print_solution(self):
        print("Current solution:")
        for row in self.board:
            print(*row)

    def create_solution(self):
        for word_index in range(len(self.board)):
            for char_index in range(len(self.board[word_index])):
                if str(self.board[word_index][char_index]) in self.letters.keys():
                    self.board[word_index][char_index] = self.letters.get(str(self.board[word_index][char_index]))
                if self.board[word_index][char_index] == 0:
                    self.board[word_index][char_index] = " "

if __name__ == "__main__":
    solver = AlphaPuzzleSolver("day2.json", "words_alpha.txt")
    solver.parse_board()
    solver.solve_board()