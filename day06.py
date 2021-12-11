TARGET = 7
NEW_BIRTHS = 9
DAYS = 256

def main():
    with open('data/day6.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    init_state = [int(c) for c in contents[0].split(',')]

    # it_sol = iterative_solution(init_state)
    # print(f'Iterative solution: {it_sol}')
    rec_sol = recursive_solution(init_state)
    print(f'Recursive solution: {rec_sol}')

def iterative_solution(init_state):
    list_times = init_state
    for d in range(1, DAYS + 1):
        # Decrease by 1 every entry that is not 0 on list_times
        new_list = []
        add_babies = []
        for l in list_times:
            if l > 0:
                new_list.append(l-1)
            if l == 0:
                new_list.append(TARGET-1)
                add_babies.append(NEW_BIRTHS-1)
        list_times = new_list + add_babies
    # print(f'After {d} days: {list_times}')
    return len(list_times)

def recursive_solution(init_state):
    cnt = 0
    table = {}
    for l in init_state:
        cnt += recursive(0, l, table)
    return cnt

def recursive(d, val, table = {}):
    if d == DAYS:
        return 1
    if val > 0:
        return recursive(d+1, val-1, table)
    if val == 0:
        if d in table:
            return table[d]
        else:
            table[d] = recursive(d+1, TARGET-1, table) + \
                       recursive(d+1, NEW_BIRTHS-1, table)
            return table[d]


if __name__ == '__main__':
    main()
