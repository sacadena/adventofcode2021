def main():
    with open('data/day01.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents]
    numbers = [int(c) for c in contents]
    asw1 = puzzle1(numbers)
    print(f'(Puzzle 1) Number of increments: {asw1}')
    asw2 = puzzle2(numbers)
    print(f'(Puzzle 2) Number of increments aggr.: {asw2}')

def puzzle1(numbers):
    diffs = [n1 - n2 for n1, n2 in zip(numbers[1:], numbers[:-1])]
    return sum([d > 0 for d in diffs])

def puzzle2(numbers, k = 3):
    convolved_nums = []
    for i in range(len(numbers) - k + 1):
        convolved_nums.append(sum(numbers[i:i+k]))
    return puzzle1(convolved_nums)

if __name__ == '__main__':
    main()
