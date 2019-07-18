import json


class AlphaPuzzleSolver:

    h_word_list = []
    v_word_list = []

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.board = puzzle.get("board")

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
                    word.append(index)
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
                    word.append(self.board[index][column])
            if len(word) > 1:
                self.v_word_list.append(word)
                word = []
            elif len(word) < 2:
                word = []

        print(self.h_word_list)
        print(self.v_word_list)
    #
    # def substitutor(self, puzzle):
    #     for num in puzzle.get("letters"):
    #         for

    def word_search(self, partial_word):
        possible_words = []

if __name__ == "__main__":
    with open("day1.json", 'r') as f:
        day_1 = json.load(f)
    solver = AlphaPuzzleSolver(day_1)
    solver.parse_board()
