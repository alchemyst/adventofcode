from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

instructions = []

with open(filename) as f:
    for line in f:
        line = line.strip().split()
        line.remove('->')
        instructions.append(tuple(line))


def emulate(instructions):
    wires = {}
    queue = instructions.copy()

    def check(instruction, inputs):
        for input in inputs:
            if not input.isdigit() and input not in wires:
                queue.append(instruction)
                return False
        return True

    def value(signal):
        if signal.isdigit():
            return int(signal)
        else:
            return wires[signal]

    while queue:
        instruction = queue.pop(0)

        match instruction:
            case signal, outwire:
                if check(instruction, [signal]):
                    wires[outwire] = value(signal) & 0xFFFF
            case "NOT", inwire, outwire:
                if check(instruction, [inwire]):
                    wires[outwire] = ~value(inwire) & 0xFFFF
            case inwire1, "AND", inwire2, outwire:
                if check(instruction, [inwire1, inwire2]):
                    wires[outwire] = (value(inwire1) & value(inwire2)) & 0xFFFF
            case inwire1, "OR", inwire2, outwire:
                if check(instruction, [inwire1, inwire2]):
                    wires[outwire] = (value(inwire1) | value(inwire2)) & 0xFFFF
            case inwire, "LSHIFT", shift, outwire:
                if check(instruction, [inwire, shift]):
                    wires[outwire] = (value(inwire) << value(shift)) & 0xFFFF
            case inwire, "RSHIFT", shift, outwire:
                if check(instruction, [inwire, shift]):
                    wires[outwire] = (value(inwire) >> value(shift)) & 0xFFFF

    return wires

# Part 2
wires = emulate(instructions)
solution(wires['a'])

# Part 2
instructions = [instruction for instruction in instructions if instruction[-1] != 'b']
instructions.append((str(wires['a']), 'b'))

new_wires = emulate(instructions)
solution(new_wires['a'])