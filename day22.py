import re
from itertools import starmap


def main():
    with open('data/day22.txt') as h:
        contents = h.read()
    contents = contents.strip().split('\n')
    instructions = list(map(parse, contents))

    # Puzzle 1
    asw1 = reboot(instructions, initialize_reactor(50))
    print(f'(Puzzle 1) Number of cuboids on after initialization: {asw1}')

    # Puzzle 2
    asw2 = reboot(instructions, initialize_reactor(1e10))
    print(f'(Puzzle 2) Number of cuboids after whole reboot: {asw2}')


def initialize_reactor(l):
    return Cube((-l, -l, -l), (l+1, l+1, l+1), False)

def split(start, end, point):
    x0, y0, z0 = start
    x1, y1, z1 = end
    px, py, pz = point
    out = [((x0, y0, z0), (px, py, pz)),
           ((px, y0, z0), (x1, py, pz)),
           ((x0, y0, pz), (px, py, z1)),
           ((px, y0, pz), (x1, py, z1)),
           ((x0, py, z0), (px, y1, pz)),
           ((px, py, z0), (x1, y1, pz)),
           ((x0, py, pz), (px, y1, z1)),
           ((px, py, pz), (x1, y1, z1))]
    return out

def coners(n, nmin, nmax):
    return max(min(n, nmax), nmin)

def parse(line):
    x0, x1, y0, y1, z0, z1 = map(int, re.findall(r'-?\d+', line))
    start, end = (x0, y0, z0), (x1 + 1, y1 + 1, z1 + 1)
    on = line.startswith('on')
    return Cube(start, end, on)

def reboot(list_cubes, reactor):
    for cube in list_cubes:
        reactor.toggle(cube.intersect(reactor))
    return reactor.count_on()

class Cube:
    def __init__(self, start, end, on):
        self.start = start
        self.end = end
        self.on = on
        self.children = []

    def split(self, point):
        for (start, end) in split(self.start, self.end, point):
            child = Cube(start, end, self.on)
            if child.size():
                self.children.append(child)

    def toggle(self, subset):
        if subset.size():
            if self.children:
                for child in self.children:
                    child.toggle(subset.intersect(child))
            elif subset.on != self.on:
                if subset.start == self.start:
                    if subset.end == self.end:
                        self.on = subset.on
                    else:
                        self.split(subset.end)
                        self.children[0].on = subset.on
                else:
                    self.split(subset.start)
                    self.children[-1].toggle(subset)

    def size(self):
        dx, dy, dz = (e - s for s, e in zip(self.start, self.end))
        return int(dx * dy * dz)

    def count_on(self):
        if self.children:
            return sum(child.count_on() for child in self.children)
        return self.on * self.size()

    def intersect(self, to):
        start = tuple(starmap(coners, zip(self.start, to.start, to.end)))
        end = tuple(starmap(coners, zip(self.end, to.start, to.end)))
        return Cube(start, end, self.on)


if __name__ == '__main__':
    main()
