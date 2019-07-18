import json



def parse_puzzle(puzzle):
    word = []
    h_word_list = []
    v_word_list = []
    board = puzzle.get("board")
    for row in board:
        for index in row:
            if index == 0 and len(word) > 1:
                h_word_list.append(word)
                word = []
            elif index == 0 and len(word) < 2:
                word = []
            elif not index == 0:
                word.append(index)
        if len(word) > 1:
            h_word_list.append(word)
            word = []
        elif len(word) < 2:
            word = []

    word = []

    for column in range(len(board[0])):
        for index in range(len(board)):
            if board[index][column] == 0 and len(word) > 1:
                v_word_list.append(word)
                word = []
            elif board[index][column] == 0 and len(word) < 2:
                word = []
            elif not board[index][column] == 0:
                word.append(board[index][column])
        if len(word) > 1:
            v_word_list.append(word)
            word = []
        elif len(word) < 2:
            word = []


    print(h_word_list)
    print(v_word_list)
#
# def substitutor(puzzle):
#     for num in puzzle.get("letters"):
#         for

#def solve(puzzle):
if __name__ == "__main__":
    with open("day1.json", 'r') as f:
        day_1 = json.load(f)
    parse_puzzle(day_1)
