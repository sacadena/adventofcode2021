from math import floor, ceil

def main():
    with open('data/day17.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents][0]
    contents = contents.split('target area: ')[1]
    contents_x = contents.split(', ')[0].split('x=')[1].split('..')
    contents_y = contents.split(', ')[1].split('y=')[1].split('..')
    target_x = [int(c) for c in contents_x]
    target_y = [int(c) for c in contents_y]

    # Puzzle 1
    xval, yval = initial_velocity_max_yspeed(target_x, target_y)
    assert valid_initial_vel([xval, yval], target_x, target_y), "Found values don't hit target"
    asw1 = int(yval * (yval + 1) / 2)
    print(f'(Puzzle 1) The max y value reached: {asw1}')

    # Puzzle 2
    possible_points = find_possible_points(target_x, target_y)
    for p in possible_points:
        assert valid_initial_vel(p, target_x, target_y), f'Unvalid initial vel: {p}'
    asw2 = len(possible_points)
    print(f'(Puzzle 2) Number of possible initial velocities: {asw2}')


def find_possible_points(target_x, target_y):
    possible_points = set()
    stable_x_points = set()
    maxx = ceil((-1 + (1 + 8 * target_x[1]) ** 0.5) / 2)  # max x value
    n = 1
    while n < 1000:  # Should think of better stopping criterium
        target_to_val = lambda n, t: (n * (n - 1) / 2 + t) / n
        lowy, highy = target_to_val(n, target_y[0]), target_to_val(n, target_y[1])
        ints_y = contained_integers(lowy, highy)
        lowx, highx = target_to_val(n, target_x[0]), target_to_val(n, target_x[1])

        if n > maxx:
            ints_x = list(stable_x_points)  # Use previous values that hit the target
        else:
            ints_x = contained_integers(lowx, highx)
            for i in ints_x:
                if n >= i:
                    stable_x_points.add(i)  # add x vals if the number of steps is larger

        for x in ints_x:
            for y in ints_y:
                possible_points.add((x, y))
        n += 1

    return possible_points


def contained_integers(low, high):
    out = []
    for i in range(ceil(low), ceil(high)):
        out.append(i)
    if int(high) == high:
        out.append(high)
    return out


def initial_velocity_max_yspeed(target_x, target_y):
    xval = int((-1 + (1 + 4*target_x[0]*2)**0.5)/ 2) + 1
    maxyval = -float('inf')
    min_y = min([abs(t) for t in target_y])
    max_y = max([abs(t) for t in target_y])

    for yval in range(min_y, max_y+1):
        if valid_initial_vel([xval, yval], target_x, target_y):
            if yval > maxyval:
                maxyval = yval
            else:
                return xval, maxyval
    return xval, maxyval


def valid_initial_vel(velocities, target_x, target_y, verbose=False):
    x, y = 0, 0
    velx, vely = velocities
    while x <= target_x[1] and y >= target_y[0]:
        if x >= target_x[0] and y <= target_y[1]:
            if verbose:
                print(x, y)
            return True

        x += velx
        y += vely

        if velx > 0:
            velx -= 1
        elif velx < 0:
            velx += 1
        vely -= 1
    return False


if __name__ == '__main__':
    main()
