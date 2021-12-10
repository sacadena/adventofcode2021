# https://adventofcode.com/2021/day/9
def main():
    with open('day9.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    contents = [[int(ci) for ci in c] for c in contents]

    asw1 = puzzle1(contents)
    print(f'(Puzzle 1) risk level: {asw1}')

    asw2 = puzzle2(contents, 3)
    print(f'(Puzzle 2) The product of the count of the 3 largest basins: {asw2}')

def puzzle2(contents, k=3):
    lows = find_lows(contents)
    cnts = []
    visited = set()
    for loc in lows:
        cnts.append(count(contents, loc, visited))
    return prod(sorted(cnts)[-k:])

def puzzle1(contents):
    lows = find_lows(contents)
    risk = 0
    for loc in lows:
        r, c = loc
        risk += contents[r][c] + 1
    return risk

def find_lows(contents):
    w, h = len(contents[0]), len(contents)
    lows = []
    for row in range(h):
        for col in range(w):
            min = min_neighbours(row, col, contents)
            if contents[row][col] < min:
                lows.append([row, col])
    return lows

def prod(vals):
    p = 1
    for v in vals:
        p *= v
    return p

def count(contents, loc, visited):
    r,c = loc
    w, h = len(contents[0]), len(contents)
    if contents[r][c] == 9:
        return 0
    visited.add(','.join([str(r), str(c)]))
    directions = [[r-1, c], [r+1, c], [r, c-1], [r, c+1]]
    sum = 1
    for dir in directions:
        x, y = dir
        if ','.join([str(x), str(y)]) in visited:
            continue
        if x < 0 or x >= h:
            continue
        if y < 0 or y >= w:
            continue
        sum += count(contents, dir, visited)
    return sum

def min_neighbours(row, col, contents):
    w, h = len(contents[0]), len(contents)
    neighbours = []
    pairs = [[row-1, col], [row+1, col], [row, col-1], [row, col+1]]
    for pair in pairs:
        r, c = pair
        if r < 0 or r >= h:
            continue
        if c < 0 or c >= w:
            continue
        neighbours.append(contents[r][c])
    return min(neighbours)


if __name__ == '__main__':
    main()
