from math import floor, ceil
import re
from itertools import permutations

def main():
    with open('data/day18.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    # Puzzle 1
    res = contents[0]
    for c in contents[1:]:
        res = add_snailfish(res, c)

    asw1 = magnitude(res)
    print(f'(Puzzle 1) the magnitude of the sum is: {asw1}')

     # Puzzle 2
    mags = []
    for a, b in permutations(contents, 2):
        mags.append(magnitude(add_snailfish(a, b)))
    asw2 = max(mags)
    print(f'(Puzzle 2) the max magnitude of pairs: {asw2}')


def magnitude(x):
    while x.count(",") > 1:
        for p in re.findall("\[\d+,\d+\]", x):
            pair = re.search(re.escape(p), x)
            left_digit, right_digit = p[1:-1].split(",")
            x = f"{x[: pair.start()]}{int(left_digit) * 3 + int(right_digit) * 2}{x[pair.end() :]}"
    left_digit, right_digit = x[1:-1].split(",")
    return int(left_digit) * 3 + int(right_digit) * 2


def add_snailfish(a, b):

    x = f'[{a},{b}]'
    if is_reduced(x):
        return x
    else:
        x = reduce(x)
    return x


def reduce(x):
    cnp = ind_nested_pairs(x)
    hlrn = ind_large_regular_number(x)
    if cnp is not None:
        x = explode_first_pair(x)
        return reduce(x)
    if hlrn is not None:
        x = split(x)
        return reduce(x)
    return x


def is_reduced(x):
    return (ind_nested_pairs(x) is None) and \
           (ind_large_regular_number(x) is None)


def ind_nested_pairs(x):
    cnt_brkts = 0
    for j, c in enumerate(x):
        if c == '[':
            cnt_brkts += 1
        if c == ']':
            cnt_brkts -= 1
        if cnt_brkts > 4:
            return j
    return None


def ind_large_regular_number(x):
    len_num = 2
    res = ""
    for idx in range(len(x) - len_num + 1):
        is_num = True
        for j in range(len_num):
            is_num = is_num & x[idx + j].isdigit()

        if is_num :
            return idx
    return None


def explode_first_pair(x):
    offset = 0
    for p in re.findall("\[\d+,\d+\]", x):
        pair = re.search(re.escape(p), x[offset:])
        left_brackets = x[: pair.start() + offset].count("[")
        right_brackets = x[: pair.start() + offset].count("]")
        if left_brackets - right_brackets >= 4:
            a, b = pair.group()[1:-1].split(",")
            left = x[: pair.start() + offset][::-1]
            right = x[pair.end() + offset :]

            search_left = re.search("\d+", left)
            if search_left:
                amt = int(left[search_left.start() : search_left.end()][::-1]) + int(a)
                left = f"{left[:search_left.start()]}{str(amt)[::-1]}{left[search_left.end():]}"

            search_right = re.search("\d+", right)
            if search_right:
                amt = int(right[search_right.start() : search_right.end()]) + int(b)
                right = (
                    f"{right[:search_right.start()]}{amt}{right[search_right.end():]}"
                )

            x = f"{left[::-1]}0{right}"
            break
        else:
            offset = pair.end() + offset
    return x


def split(x):
    ind = ind_large_regular_number(x)
    val = int(x[ind: ind + 2])
    x = list(x)
    x[ind: ind + 2] = f'[{floor(val / 2)},{ceil(val / 2)}]'
    x = ''.join(x)  # Turn list to string
    return x


if __name__ == '__main__':
    main()
