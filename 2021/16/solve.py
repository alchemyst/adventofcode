from aoc import solution

class BitStream:
    def __init__(self, bitstring):
        self.bitstring = bitstring
        self.position = 0

    def at_end(self):
        return self.position == len(self.bitstring)

    def read(self, bits, convert=False):
        part = self.bitstring[self.position:self.position + bits]
        self.position += bits
        # print('Read part: ', part)
        if convert:
            return int(part, 2)
        else:
            return part

    def __str__(self):
        return self.bitstring


class Literal:
    def __init__(self, version, type_id, stream: BitStream):
        self.version = version
        self.type_id = type_id

        value = ''
        while True:
            part = stream.read(5)
            value += part[1:]
            if part.startswith('0'):
                break

        self.binvalue = value
        self.value = int(value, 2)

    def __repr__(self):
        return f'Literal(version={self.version}, value={self.value})'

    def versionsum(self):
        return self.version

class Operator:
    def __init__(self, version, type_id, contents):
        self.version = version
        self.type_id = type_id
        self.contents = contents

    @property
    def value(self):
        subvalues = [p.value for p in self.contents]
        match self.type_id:
            case 0:
                return sum(subvalues)
            case 1:
                prod = subvalues[0]
                for v in subvalues[1:]:
                    prod *= v
                return prod
            case 2:
                return min(subvalues)
            case 3:
                return max(subvalues)
            case 5:
                return int(subvalues[0] > subvalues[1])
            case 6:
                return int(subvalues[0] < subvalues[1])
            case 7:
                return int(subvalues[0] == subvalues[1])

    def __repr__(self):
        return f'Operator(version={self.version}, contents={self.contents})'

    def versionsum(self):
        return self.version + sum(p.versionsum() for p in self.contents)

def parse(stream: BitStream):
    # take first three bits off the stream
    # print('Parsing...')
    version = stream.read(3, True)
    # print(f'{version=}')
    type_id = stream.read(3, True)
    # print(f'{type_id=}')

    if type_id == 4:
        return Literal(version, type_id, stream)

    length_type_id = stream.read(1)
    if length_type_id == '0':
        total_length_in_bits = stream.read(15, True)
        # if debug:
        #     print(f'{total_length_in_bits=}')
        packet_stream = BitStream(stream.read(total_length_in_bits))
        contents = []
        while True:
            packet = parse(packet_stream)
            contents.append(packet)
            if packet_stream.at_end():
                break

        return Operator(version, type_id, contents)
    else:
        number_of_subpackets = stream.read(11, True)
        # if debug:
        #     print(f'{number_of_subpackets=}')
        contents = []
        for _ in range(number_of_subpackets):
            packet = parse(stream)
            contents.append(packet)
        return Operator(version, type_id, contents)

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    transmission = f.read().strip()

# # Example 1
# transmission = 'D2FE28'
# # Example 2
# transmission = '38006F45291200'
# # Example 3
# transmission = 'EE00D40C823060'
# # Example 4
# transmission = '8A004A801A8002F478'
bits = ''.join(f'{int(c, base=16):04b}' for c in transmission)

# print(transmission)
# print(bits)

contents = parse(BitStream(bits))

# print(contents)
solution(contents.versionsum())

solution(contents.value)