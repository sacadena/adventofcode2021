def main():
    with open('data/day02.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]

    directions = [c.split(' ')[0] for c in contents]
    steps = [int(c.split(' ')[1]) for c in contents]

    asw1 = puzzle1(directions, steps)
    print(f'(Puzzle 1) Horz pos. x Vert pos.: {asw1}')
    asw2 = puzzle2(directions, steps)
    print(f'(Puzzle 2) Horz pos. x Vert pos.: {asw2}')

def puzzle1(directions, steps):
    x, y = 0, 0
    for dir, step in zip(directions, steps):
        if dir == 'forward':
            x += step
        elif dir == 'down':
            y += step
        elif dir == 'up':
            y -= step
        else:
            raise ValueError
    return x * y

def puzzle2(directions, steps):
    x, y, aim = 0, 0, 0
    for dir, step in zip(directions, steps):
        if dir == 'down':
            aim += step
        elif dir  == 'up':
            aim -= step
        elif dir == 'forward':
            x += step
            y += aim * step
        else:
            raise ValueError
    return x * y

if __name__ == '__main__':
    main()
