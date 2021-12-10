# https://adventofcode.com/2021/day/10

OPEN_TO_CLOSE = {'(': ')', '[': ']', '{': '}', '<': '>'}
COST_WRONG_CHAR = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORE_COMPLETE_CHAR = {')': 1, ']': 2, '}': 3, '>': 4}

def main():
    with open('day10.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    wrong_chars = []
    incomplete_lines = []
    for line in contents:
        ch = find_wrong_chars(line)
        if ch is not None:
            wrong_chars.append(ch)
        else:
            incomplete_lines.append(line)

    asw1 = compute_cost(wrong_chars)
    print(f'(Puzzle1) The total cost of illegal chars: {asw1}')

    scores = []
    for line in incomplete_lines:
        remain = complete_line(line)
        scores.append(compute_score(remain))

    asw2 = sorted(scores)[len(scores) // 2]
    print(f'(Puzzle 2) The middle score of remaining is: {asw2}')


def compute_score(remain):
    score = 0
    for ch in remain:
        score = SCORE_COMPLETE_CHAR[ch] + (score * 5)
    return score

def complete_line(line):
    stack_chars = []
    for ch in line:
        if ch in OPEN_TO_CLOSE.keys():
            stack_chars.append(ch)
        if ch == OPEN_TO_CLOSE[stack_chars[-1]]:
            stack_chars.pop()
    if not stack_chars:
        return ''
    return ''.join([OPEN_TO_CLOSE[ch] for ch in stack_chars[::-1]])

def compute_cost(wrong_chars):
    return sum([COST_WRONG_CHAR[ch] for ch in wrong_chars])

def find_wrong_chars(line: str):
    stack_chars = []
    for ch in line:
        if (not stack_chars) and (ch in OPEN_TO_CLOSE.values()):  # check starting wrong
            return ch
        if ch in OPEN_TO_CLOSE.keys():
            stack_chars.append(ch)
            continue
        if ch == OPEN_TO_CLOSE[stack_chars[-1]]:
            stack_chars.pop()
            continue
        return ch
    return None

if __name__ == '__main__':
    main()
