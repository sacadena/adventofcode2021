def main():
    with open('day7.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    locations = [int(c) for c in contents[0].split(',')]
    asw1 = puzzle1(locations)
    asw2 = puzzle2(locations)

    print(f'Answer puzzle1: {asw1}')
    print(f'Answer puzzle2: {asw2}')

def median(values):
    sorted_vals = sorted(values)
    N = len(sorted_vals)
    if N % 2 == 0:
        return (sorted_vals[N//2 - 1] + sorted_vals[N//2]) / 2
    else:
        return sorted_vals[N//2]

def puzzle1(locations):
    m = median(locations)
    return int(sum([abs(x - m) for x in locations]))

def puzzle2(locations):
    sorted_locations = sorted(locations)
    low, up = sorted_locations[0], sorted_locations[-1]
    while up - low > 1:
        ld = compute_cost(low, sorted_locations)
        ud = compute_cost(up, sorted_locations)

        mid = (up - low)//2 + low
        if ud < ld:
            low = mid
        elif ud > ld:
            up = mid
        else:
            break
    return compute_cost(mid, sorted_locations)

def compute_cost(x, locs):
    distance = lambda l, p: ((l-p)**2 + abs(l-p)) // 2
    return sum([distance(si, x) for si in locs])

if __name__ == '__main__':
    main()
