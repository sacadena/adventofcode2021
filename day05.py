# https://adventofcode.com/2021/day/5#part2
from collections import defaultdict

def main():
    with open('data/day5.txt') as h:
        contents = h.readlines()
    contents  = [c.split('\n')[0] for c in contents]

    start, end = zip(*[c.split(' -> ') for c in contents])
    start = [v.split(',') for v in start]
    end = [v.split(',') for v in end]

    asw1 = puzzle1(start, end)
    asw2 = puzzle2(start, end)
    print(f'Number of Multiple hits (Puzzle 1): {asw1}')
    print(f'Number of Multiple hits (Puzzle 2): {asw2}')

def puzzle1(start, end):
    """ Only horizontal lines are allowed """
    points_covered = defaultdict(int)
    for s, e in zip(start, end):

        # Turn strings into numbers
        s = [int(si) for si in s]
        e = [int(ei) for ei in e]

        # filter s, e that don't represent horz, vert lines
        if (s[0] !=  e[0]) and (s[1] != e[1]):
            continue

        # generate list of points between s and e
        x_range = sorted([s[0], e[0]])
        y_range = sorted([s[1], e[1]])
        points = [[x, y] for x in
                    range(x_range[0], x_range[1] + 1)
                        for y in range(y_range[0], y_range[1] + 1)]

        # add each point to points_covered keys with +1 as val
        for p in points:
            key = ','.join([str(pi) for pi in p])
            points_covered[key] += 1

    # Count multiple hits
    multiple_hits = sum([hit > 1 for hit in points_covered.values()])
    return multiple_hits

def puzzle2(start, end):
    """ Horizontal, vertical, and diagonal (45 deg) allowd """
    points_covered = defaultdict(int)
    for s, e in zip(start, end):
        # Turn strings into numbers
        s = [int(si) for si in s]
        e = [int(ei) for ei in e]

        dx = e[0] - s[0]
        dy = e[1] - s[1]
        # Check if vertical lines:
        if s[1] == e[1]:  # vertical
            val_range = sorted([s[0], e[0]])
            points = [[x, s[1]] for x in
                            range(val_range[0], val_range[1] + 1)]

        elif s[0] == e[0]:  # horizontal
            val_range = sorted([s[1], e[1]])
            points = [[s[0], y] for y in
                            range(val_range[0], val_range[1] + 1)]


        elif abs(dx) == abs(dy):  # diagonal
            stepx = 1 if dx > 0 else -1
            stepy = 1 if dy > 0 else -1
            points = [[x,y] for x, y in
                        zip(range(s[0], e[0] + stepx, stepx),
                            range(s[1], e[1] + stepy, stepy))]
        else:
            continue

        # add each point to points_covered keys with +1 as val
        for p in points:
            key = ','.join([str(pi) for pi in p])
            points_covered[key] += 1

    # Count multiple hits
    multiple_hits = sum([hit > 1 for hit in points_covered.values()])
    return multiple_hits


if __name__ == '__main__':
    main()
