from copy import deepcopy
def main():
    with open('data/day13.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    points = [c for c in contents if c and ('fold' not in c)]
    instructions = [c for c in contents if ('fold' in c)]

    points = [[int(pi) for pi in p.split(',')] for p in points]
    instr_axis = [inst.split('=')[0][-1] for inst in instructions]
    instr_val = [int(inst.split('=')[1]) for inst in instructions]

    # Problem 1:
    pnts = fold_map(points, instr_axis[:1], instr_val[:1])
    asw1 = len(pnts)
    print(f'(Puzzle 1) After the first fold, there are {asw1} points')

    # Problem 2:
    pnts = fold_map(points, instr_axis, instr_val)
    print(f'(Puzzle 2) The code can be read here: \n\n')
    print_map(pnts)
    print()


def fold_map(points, instr_axis, instr_val):
    points = deepcopy(points)
    for axis, val in zip(instr_axis, instr_val):
        if axis == 'y':
            pnts = [p for p in points if p[1] < val]
            new_points = [[p[0], 2*val - p[1]] for p in points if p[1] > val]
        else:
            pnts = [p for p in points if p[0] < val]
            new_points = [[2*val - p[0], p[1]] for p in points if p[0] > val]

        for np in new_points:
            if np not in pnts:
                pnts.append(np)
        points = pnts

    return points


def print_map(points):
    X = max([p[0] for p in points])+1
    Y = max([p[1] for p in points])+1
    map = [['.']*X for _ in range(Y)]
    for (x,y) in points:
        map[y][x] = '#'
    print('\n'.join([''.join(r) for r in map]))

if __name__ == '__main__':
    main()
