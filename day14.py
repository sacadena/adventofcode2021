from copy import copy
from collections import defaultdict

def main():
    with open('data/day14.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    template = contents[0]
    pair_insertion = contents[2:]

    map = dict()
    [map.update({p.split(' -> ')[0]: p.split(' -> ')[1]}) for p in pair_insertion];

    asw1 = recursive_solution(template, map, 10)
    print(f'(Puzzle 1) The spread of most and least common element for 10 steps: {asw1}')
    asw2 = recursive_solution(template, map, 40)
    print(f'(Puzzle 2) The spread of most and least common element for 40 steps: {asw2}')

def recursive_solution(template, map, n_steps = 40):
    chars = set(map.values())
    # Initialize the count for each char with the last letter of the sequence
    current_count = {ch: 1 if template[-1:] == ch else 0 for ch in chars}
    for i in range(len(template)-1):
        cnt_this = count(template[i:i+2], n_steps, map)  # count how many for this pair
        current_count = sum_counts(cnt_this, current_count)  # accumulate counts
    return max(current_count.values()) - min(current_count.values())

def sum_counts(cnt1, cnt2):
    output = dict()
    for ch in cnt1:
        output[ch] = cnt1[ch] + cnt2[ch]
    return output

def count(pair, num_steps, map, table = dict()):
    """ Recursive function. Counts for a single pair all descendent symbols """
    chars = set(map.values())
    if num_steps == 0:
        return {ch: 1 if pair[:1] == ch else 0 for ch in chars}

    key = pair + '{:04d}'.format(num_steps)
    if key in table:
        return table[key]

    p1 = pair[:1] + map[pair]
    p2 = map[pair] + pair[1:]

    cnt1 = count(p1, num_steps - 1, map, table)
    cnt2 = count(p2, num_steps - 1, map, table)

    table[key] = sum_counts(cnt1, cnt2)

    return table[key]

def iterative_solution(template, map, n_steps = 10):
    """ Solution with O(n*k^2) where k = n_steps """
    temmplate = copy(template)
    for step in range(n_steps):
        new_template = ''
        for i in range(len(template)-1):
            new_template += template[i:i+1] + map[template[i:i+2]] #+ template[i+1:i+2]
        new_template += template[-1]
        template = new_template
    counter  = defaultdict(int)
    for ch in template:
        counter[ch] += 1
    return max(counter.values()) - min(counter.values())

if __name__ == '__main__':
    main()
