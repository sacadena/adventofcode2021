from collections import defaultdict
from copy import copy

def main():
    with open('day3.txt') as data:
        instructions = data.readlines()

    bit_nums = [line.split('\n')[0] for line in instructions]
    num_positions = len(bit_nums[0])

    # filter based on 1s
    list1 = copy(bit_nums)
    for pos in range(num_positions):
        num_ones = count_ones(list1, pos)
        num_zeros = len(list1) - num_ones
        if num_ones >= num_zeros:
            list1 = [line for line in list1 if int(line[pos]) == 1]
        else:
            list1 = [line for line in list1 if int(line[pos]) == 0]
        if len(list1) == 1:
            break

    # Filter based on 0s
    list2 = copy(bit_nums)
    for pos in range(num_positions):
        num_ones = count_ones(list2, pos)
        num_zeros = len(list2) - num_ones
        if num_zeros <= num_ones:
            list2 = [line for line in list2 if int(line[pos]) == 0]
        else:
            list2 = [line for line in list2 if int(line[pos]) == 1]
        if len(list2) == 1:
            break

    assert (len(list1) == 1) and (len(list2) == 1)
    val1 = binary_to_decimal(list1[0])
    val2 = binary_to_decimal(list2[0])

    print(f'Oxigen: {val1}')
    print(f'CO2 Scrubber: {val2}')
    print(f'Product: {val1 * val2}')


def binary_to_decimal(num: str):
    return sum([2**j for j, c in enumerate(num[::-1]) if int(c) == 1])

def count_ones(list_string_nums: str, position: int):
    counts = 0
    for num in list_string_nums:
        counts += int(num[position])
    return counts


if __name__ == '__main__':
    main()
