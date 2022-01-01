from copy import deepcopy

def main():
    with open('data/day20.txt') as h:
        contents = h.read()
    contents = contents.strip().split('\n')
    code = contents[0]
    image = contents[2:]

    # Puzzle 1
    pad_val = '.'
    outimg, pad_val = enhance(image, code, pad_val)
    outimg, pad_val = enhance(outimg, code, pad_val)
    asw1 = count_symbols(outimg, pad_val)
    print(f'(Puzzle 1) Number of # symbols after 2 enchancements: {asw1}')

    # Puzzle 2
    pad_val = '.'
    outimg = image
    for i in range(50):
        outimg, pad_val = enhance(outimg, code, pad_val)
    asw2 = count_symbols(outimg, pad_val)
    print(f'(Puzzle 2) Number of # symbols after 50 enhancements: {asw2}')
    print_image(outimg)


def count_symbols(image, pad_val='.'):
    if pad_val == '.':
        return sum([sum([i == '#' for i in row]) for row in image])
    return float('inf')

def enhance(image, code, pad_value = '.'):
    padimg = pad_image(image, val = pad_value, p=2)

    if pad_value == '.':
        pad_value = code[0:1]
    else:
        pad_value = code[-1:]

    outimg = pad_image(image, val = pad_value, p=1)
    outimg = [list(r) for r in outimg]

    for i in range(1, len(padimg)-1):
        for j in range(1, len(padimg[0])-1):
            x = ''.join([row[j-1:j+2] for row in padimg[i-1:i+2]])
            x = ''.join(['0' if c == '.' else '1' for c in list(x)])
            idx = int(x, 2)
            val = code[idx:idx+1]
            outimg[i-1][j-1] = val

    outimg = [''.join(row) for row in outimg]
    return outimg, pad_value

def print_image(x):
    for r in x:
        print(r)

def pad_image(image, val = '.', p=1):
    m, n = len(image), len(image[0])
    new_image = deepcopy(image)
    for i, row in enumerate(new_image):
        new_image[i]  = val*p + row + val*p
    for _ in range(p):
        new_image.insert(0, val*(2*p + n))
        new_image.append(val*(2*p + n))
    return new_image


if __name__ == '__main__':
    main()
