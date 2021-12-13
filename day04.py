# https://adventofcode.com/2021/day/4#part2
import numpy as np
from copy import copy

def main():
    # Reading and formatting
    with open('data/day04.txt') as h:
        contents = h.readlines()

    contents = [c.split('\n')[0] for c in contents]
    order = [int(c) for c in contents[0].split(',')]

    boards, board = [], []
    for line in contents[2:]:
        if line == '':
            boards.append(board)
            board = []
        else:
            board.append([int(l) for l in line.split(' ') if l != ''])

    total1 = puzzle1(order, boards)
    total2 = puzzle2(order, boards)
    print(f'Puzzle 1: {total1}')
    print(f'Puzzle 2: {total2}')

# puzzle 1
def puzzle1(order: list, boards: list):
    """ Pick the winning board """
    marks = set()
    for num in order:
        marks.add(num)
        for b in boards:
            if is_row_marked(b, marks) or is_col_marked(b, marks):
                s = sum_not_marked(b, marks)
                return s * num

    print('No board won')
    return -1

def puzzle2(order: list, boards: list):
    """ Pick the board that would be the last to win """
    boards = copy(boards)
    marks = set()
    for num in order:
        marks.add(num)
        i = 0
        while (len(boards) > 1) and (i < len(boards)):
            b = boards[i]
            if is_row_marked(b, marks) or is_col_marked(b, marks):
                boards = [b for j, b in enumerate(boards) if j != i]
            else:
                i += 1

        if len(boards) == 1:
            b = boards[0]
            if is_row_marked(b, marks) or is_col_marked(b, marks):
                s = sum_not_marked(b, marks)
                return s * num

    print('Something went wrong')
    return -1

def is_row_marked(board, marks):
    for row in board:
        if sum([r in marks for r in row]) == len(row):
            return True
    return False

def is_col_marked(board, marks):
    assert len(board[0]) == len(board)
    n = len(board)
    board_transpose = [[row[i] for row in board] for i in range(n)]
    return is_row_marked(board_transpose, marks)

def sum_not_marked(board, marks):
    n = len(board)
    return sum([sum([row[i] for row in board if row[i] not in marks]) for i in range(n)])

if __name__ == '__main__':
    main()
