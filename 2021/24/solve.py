import pathlib
import pickle
from itertools import product

from rich.progress import track

from aoc import solution

def get_instructions(instruction_str: str):
    return [line.strip().split() for line in instruction_str.splitlines() if line.strip()]

def parse(filename):
    with open(filename) as f:
        instruction_str = f.read()

    return instruction_str

def process(instructions, inputs, invar=None):
    var = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    if invar is not None:
        var.update(invar)

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

def inp_parts(instruction_str):
    parts = []
    for line in instruction_str.splitlines():
        line = line.strip()
        if line.startswith('inp'):
            part = []
            parts.append(part)
        part.append(line.split())

    return parts

def verify_only_z(parts):
    # Check what we need to change in a part
    effects = []
    for part in parts:
        part_effects = set()
        for digit in valid_digits:
            basevalue = process(part, [digit])
            for changevar in 'xyz':
                for changeval in range(-100, 100):
                    newvalue = process(part, [digit], {changevar: changeval})
                    if basevalue != newvalue:
                        part_effects.add(changevar)
        effects.append(part_effects)

    for e in effects:
        assert e == {'z'}

    # Observation: every part is only affected by z
    # in my input there is a 'mul x 0' right after every inp
    # and a 'mul y 0' before y is ever used

    for part in parts:
        assert part[1] == ['mul', 'x', '0']
        yreferenced = False
        for instruction in part:
            if instruction[-1] == 'y':
                yreferenced = True
            if instruction == ['mul', 'y', '0']:
                assert not yreferenced
                break
    print("Verified only using z")


def valid_forward(parts):
    all_results = []

    # for the first part, z is always 0
    possible_zs = {0}

    for i, part in enumerate(parts, 1):
        print(f'Working on part {i}')
        part_results = {}
        next_possible_zs = set()
        total = len(valid_digits)*len(possible_zs)
        for digit, z in track(product(valid_digits, possible_zs), total=total):
            result = process(part, [digit], {'z': z})
            next_possible_zs.add(result['z'])
            part_results[(digit, z)] = result['z']
        all_results.append(part_results)
        possible_zs = next_possible_zs
        print(f'{len(possible_zs)=} {max(possible_zs)=} {min(possible_zs)=}')

    return all_results

def determine_valid_combos(all_results):
    #  figure out what combinations of (digit, z) leads to the
    # right values at the end
    targets = {0}
    valid_combos = []
    for i, part_results in enumerate(reversed(all_results)):
        print(f'Doing part {i} from the back')

        valid_inputs = {(ind, inz): outz for (ind, inz), outz in part_results.items() if outz in targets}
        new_targets = {inz for (ind, inz) in valid_inputs}
        print(f'{len(new_targets)=} {valid_inputs=}')
        targets = new_targets

        valid_combos.insert(0, valid_inputs)

    return valid_combos

def make_serial(valid_combos, z=0, reverse=True):
    first, *rest = valid_combos

    sorted_options = sorted(first.items(), reverse=reverse)
    valid_options = [((ind, inz), outz) for (ind, inz), outz in sorted_options if inz == z]

    if not valid_options:
        return None

    if not rest:
        return [valid_options[0][0][0]]

    for (ind, inz), outz in sorted_options:
        remaining_serial = make_serial(rest, outz, reverse=reverse)
        if not remaining_serial:
            continue

        return [ind] + remaining_serial

if __name__ == "__main__":
    all_results_cache = pathlib.Path('all_results.pickle')
    instruction_str = parse('input.txt')
    instructions = get_instructions(instruction_str)

    parts = inp_parts(instruction_str)
    valid_digits = range(1, 10)

    verify_only_z(parts)

    # So, we proceed by only using 'z' as a changeable input
    if all_results_cache.exists():
        print("Found cache - reading...")
        with all_results_cache.open('rb') as f:
            all_results = pickle.load(f)
        print('Read from cache')
    else:
        all_results = valid_forward(parts)
        with all_results_cache.open('wb') as f:
            pickle.dump(all_results, f)
        print('Wrote to cache')

    valid_combos = determine_valid_combos(all_results)

    part_1_serial = make_serial(valid_combos, z=0, reverse=True)
    solution(''.join(str(d) for d in part_1_serial))

    # Part 2
    part_2_serial = make_serial(valid_combos, z=0, reverse=False)
    solution(''.join(str(d) for d in part_2_serial))