from copy import deepcopy
def main():
    with open('data/day11.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    contents = [[int(j) for j in c] for c in contents]

    K = 100
    asw1 = puzzle1(contents, K)
    asw2 = puzzle2(contents)

    print(f'(Puzzle 1) Final count of flashes after {K} steps: {asw1}')
    print(f'(Puzzle 2) Number of steps to synchronize: {asw2}')

def puzzle1(x, K):
    x = deepcopy(x)
    counter_flashes = 0
    for k in range(K):
        x, counter_flashes = count_flashes(x, counter_flashes)
    return counter_flashes

def puzzle2(x):
    x = deepcopy(x)
    counter_flashes = 0
    step = 0
    while sum([sum(c) for c in x]) > 0:
        x, counter_flashes = count_flashes(x, counter_flashes)
        step += 1
    return step


def count_flashes(energy_levels, counter_flashes):
    h, w = len(energy_levels), len(energy_levels[0])
    flashed = []
    # visit all locs and increase 1. Store in a set the locs that flashed
    for r in range(h):
        for c in range(w):
            if energy_levels[r][c] < 9:
                energy_levels[r][c] += 1
            else:
                energy_levels[r][c] = 0
                flashed.append([r, c])
                counter_flashes += 1

    while flashed: # while flashed locs is not empty
        (r, c) = flashed.pop()
        steps = [-1, 0, 1]
        for x in steps:
            for y in steps:
                ri, ci = r + y, c + x
                if (x == y) and x == 0:
                    continue
                if (ri < 0) or (ci < 0) or (ci >= w) or (ri >= h):
                    continue
                if energy_levels[ri][ci] == 0:
                    continue
                else:
                    if energy_levels[ri][ci] < 9:
                        energy_levels[ri][ci] += 1
                    else:
                        energy_levels[ri][ci] = 0
                        flashed.insert(0, [ri, ci])
                        counter_flashes += 1

    return energy_levels, counter_flashes
    

if __name__ == '__main__':
    main()
