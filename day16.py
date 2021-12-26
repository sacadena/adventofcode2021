DEMOS = ['D2FE28',
         '38006F45291200',
         'EE00D40C823060',
         '8A004A801A8002F478',
         '620080001611562C8802118E34',
         'C0015000016115A2E0802F182340',
         'A0016C880162017C3686B18A3D4780']

HEX2BIN =  {'0':'0000',
            '1': '0001',
            '2': '0010',
            '3': '0011',
            '4': '0100',
            '5': '0101',
            '6': '0110',
            '7': '0111',
            '8': '1000',
            '9': '1001',
            'A': '1010',
            'B': '1011',
            'C': '1100',
            'D': '1101',
            'E': '1110',
            'F': '1111'}
def prod(x):
    p = 1
    for xi in x:
        p *= xi
    return p

def operate_subpackets(type_id, x):
    if type_id == 0:
        func = lambda x: sum(x)
    elif type_id == 1:
        func = lambda x: prod(x)
    elif type_id == 2:
        func = lambda x: min(x)
    elif type_id == 3:
        func = lambda x: max(x)
    elif type_id == 5:
        func = lambda x: x[0] > x[1]
    elif type_id == 6:
        func = lambda x: x[0] < x[1]
    elif type_id == 7:
        func = lambda x: x[0] == x[1]
    return func(x)

def process_packet(packet, versions=[], values=[], verbose=False):

    if packet is None:
        return ''
    if len(packet) <= 3:
        return packet

    version = int(packet[:3], 2)
    versions.append(version)
    type_id = int(packet[3:6], 2)
    rest = packet[6:]
    if type_id == 4:  # literal value
        terminate = False
        nums = ""
        while (not terminate) and (len(rest) > 3):
            terminate = not(bool(int(rest[:1])))
            nums = nums + rest[1:5]
            rest = rest[5:]
        value = int(nums, 2)
        if verbose:
            print(f'Literal value: {value}')
        values.append(value)

    else:  # operator
        length = rest[:1]
        if length == '1':  # num suppackages
            rest = rest[1:]
            num_packets = int(rest[:11], 2)
            rest = rest[11:]
            if verbose:
                print(f'Num subpackages: {num_packets}')

            new_vals = []
            for n in  range(num_packets):  # process subpacket
                rest = process_packet(rest, versions, new_vals)
            values.append(operate_subpackets(type_id, new_vals))

        elif length == '0':  # num of bits in subpackets
            rest = rest[1:]
            num_bits = int(rest[:15], 2)
            rest = rest[15:]
            current_tot_len = 0
            if verbose:
                print(f'Num bits: {num_bits}')

            new_vals = []
            while current_tot_len < num_bits:
                old_len = len(rest)
                rest = process_packet(rest, versions, new_vals)
                if rest is None:
                    break
                if len(rest) < 3:
                    break
                current_tot_len += (old_len - len(rest))
            values.append(operate_subpackets(type_id, new_vals))

    return rest


def main():
    with open('data/day16.txt') as h:
        contents = h.readlines()
    contents = [c.split('\n')[0] for c in contents][0]

    packet = contents
    #packet = DEMOS[6]  # Select a demo

    binary = ''.join([HEX2BIN[i] for i in packet])
    versions, values = [], []
    rest = process_packet(binary, versions, values)

    print(f'(Puzzle 1) The sum of versions is: {sum(versions)}')
    print(f'(Puzzle 2) The result of operations in subpackets is: {values[0]}')


if __name__ == '__main__':
    main()
