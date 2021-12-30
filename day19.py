import re
from collections import deque, Counter, defaultdict
from itertools import combinations

ROTATION_FUNCTIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (x, -z, y)
]

def main():
    with open('data/day19.txt') as h:
        contents = h.read()
    contents = contents.strip().split('\n')
    data = defaultdict(list)
    for c in contents:
        if c.startswith('--- scanner'):
            n = int(re.search("\d+", c).group())
            current = data[n]
            continue
        if c:
            current.append(tuple([int(v) for v in c.split(',')]))
    data = dict(data)

    # Puzzle 1:
    joined, scanners = join(data)
    asw1 = len(joined)
    print(f'(Puzzle 1) Number of unique beacons: {asw1}')

    #Puzzle 2:
    asw2 = max_distance(scanners)
    print(f'(Puzzle 2) Max distance scanners: {asw2}')

def find_scanner(base, rotated_scans):
    for scan in rotated_scans:
        [(diff, count)] = Counter((x2 - x1, y2 - y1, z2 - z1)
                                  for x1, y1, z1 in scan
                                  for x2, y2, z2 in base).most_common(1)
        if count >= 12:
            return diff, move(scan, *diff)
    return None, None

def rotations(scan):
    rot_scans = []
    for rot in ROTATION_FUNCTIONS:
        rot_scans.append([rot(*b) for b in scan])
    return rot_scans

def move(scan, dx, dy, dz):
    return [(x + dx, y + dy, z + dz) for x, y, z in scan]

def join(data):
    joined = set(data[0])
    scans = list(data.values())[1:]
    remaining = deque(list(rotations(scan)) for scan in scans)
    scanners = [(0, 0, 0)]

    while remaining:
        rotated_scans = remaining.popleft()
        scanner, moved = find_scanner(joined, rotated_scans)
        if scanner:
            joined |= set(moved)
            scanners.append(scanner)
        else:
            remaining.append(rotated_scans)

    return joined, scanners

def distance(x, y):
    return sum([abs(xi - yi) for xi, yi in zip(x, y)])

def max_distance(scanners):
    return max(distance(x, y) for x, y in combinations(scanners, 2))


if __name__ == '__main__':
    main()
