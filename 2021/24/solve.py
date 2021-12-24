from itertools import product
from aoc import solution

def get_instructions(instruction_str: str):
    return [line.strip().split() for line in instruction_str.splitlines() if line.strip()]

def parse(filename):
    with open(filename) as f:
        instruction_str = f.read()

    return instruction_str

def process(instructions, inputs):
    var = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    def value(item):
        if item in var:
            return var[item]
        else:
            return int(item)

    for instruction in instructions:
         match instruction:
            case 'inp', a:
                var[a] = inputs.pop(0)
            case 'add', a, b:
                var[a] += value(b)
            case 'mul', a, b:
                var[a] *= value(b)
            case 'div', a, b:
                if value(b) == 0:
                    raise Exception("Bad div = b=0")
                var[a] //= value(b)
            case 'mod', a, b:
                var[a] %= value(b)
            case 'eql', a, b:
                var[a] = int(var[a] == value(b))

    return var

if __name__ == "__main__":

    instructions = get_instructions(parse('input.txt'))
    for digits in product(reversed(range(1, 10)), repeat=14):
        var = process(instructions, list(digits))
        break
    print(var)



    # # Part 1
    # solution(len(lines))
    #
    # # Part 2
    # solution('Dummy')