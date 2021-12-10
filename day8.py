
DIGITS = {0: set(['a', 'b', 'c', 'e', 'f', 'g']),
          1: set(['c', 'f']),
          2: set(['a', 'c', 'd', 'e', 'g']),
          3: set(['a', 'c', 'd', 'f', 'g']),
          4: set(['b', 'c', 'd', 'f']),
          5: set(['a', 'b', 'd', 'f', 'g']),
          6: set(['a', 'b', 'd', 'e', 'f', 'g']),
          7: set(['a', 'c', 'f']),
          8: set(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
          9: set(['a', 'b', 'c', 'd', 'f', 'g'])}

CHARS = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

def main():
    with open('data/day8.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    list_prompts = [c.split(' | ')[0] for c in contents]
    list_outputs = [c.split(' | ')[1] for c in contents]
    list_prompts = [p.split(' ') for p in list_prompts]
    list_outputs = [o.split(' ') for o in list_outputs]

    asw1 = puzzle1(list_outputs)
    print(f'(Puzzle 1) Number of 1, 4, 7, 8 is {asw1}')

    sum_digits = 0
    for prompts, outputs in zip(list_prompts, list_outputs):
        connections = solve_connections(prompts)
        number = apply_connections(outputs, connections)
        sum_digits += number

    print(f'(Puzzle 2) Final sum of numbers: {sum_digits}')


def apply_connections(outputs: list, connections: dict):
    out_digits = []
    for out in outputs:
        segs = set([connections[s] for s in out])
        digit = [k for k, v in DIGITS.items() if v == segs][0]
        out_digits.append(str(digit))
    return int(''.join(out_digits))

def find(seg_ind: int, prompt: str, true_segments: list, current_map: dict):
    """Wether we match prompt to true segments with the current map"""
    if seg_ind == len(true_segments):
        return True
    segment = true_segments[seg_ind]
    for candidate in current_map[segment]:
        if candidate not in prompt:
            continue
        if find(seg_ind + 1, prompt.replace(candidate, ''), true_segments, current_map):
            return True
    return False

def filter_possible_numbers(nums, prompt, current_map):
    new_poss_nums = []
    for num in nums:
        if find(0, prompt, list(DIGITS[num]), current_map):
            new_poss_nums.append(num)
    return new_poss_nums

def filter_map(nums, prompt, map):
    if len(nums) > 1:
        return map
    segments = DIGITS[nums[0]]
    remaining = CHARS - segments
    new_map = {}
    for s in segments:
        new_map[s] = {p for p in set(prompt).intersection(map[s])}
    for s in remaining:
        new_map[s] = {p for p in (CHARS - set(prompt)).intersection(map[s])}
    return new_map

def solve_connections(prompts):
    # Initialize possible numbers for each element based on length:
    digit_lens = {k: len(v) for k, v in DIGITS.items()}
    possible_nums = [[k for k, v in digit_lens.items() if v == len(p)] for p in prompts]

    # Initialize assignments with all chars for each char:
    current_map = {k: CHARS for k in CHARS}

    # while the len of assignments is > 1 keep looping over prompt:
    #cnt =0
    while True:
        for i, prompt in enumerate(prompts):
            possible_nums[i] = filter_possible_numbers(possible_nums[i], prompt, current_map)
            current_map = filter_map(possible_nums[i], prompt, current_map)

            if sum([len(vals) == 1 for vals in current_map.values()]) == len(current_map):
                inverted_map = {list(v)[0]: k for k, v in current_map.items()}
                return inverted_map


def puzzle1(outputs):
    """ Count 1, 4, 7, 8 in all outputs """

    # No need to solve the whole puzzle as these
    # characters have unique lengths
    digit_lens = {k: len(v) for k, v in DIGITS.items()}
    nums = [1, 4, 7, 8]
    relevant_lens = [digit_lens[n] for n in nums]

    counts = 0
    for out in outputs:
        counts += len([s for s in out if len(s) in relevant_lens])
    return counts


if __name__ == '__main__':
    main()
