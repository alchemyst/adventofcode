from aoc import solution

VALID_DIGITS = list(range(1, 10))

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
                # if value(b) == 0:
                #     raise Exception("Bad div = b=0")
                var[a] //= value(b)
            case 'mod', a, b:
                var[a] %= value(b)
            case 'eql', a, b:
                var[a] = int(var[a] == value(b))
            # Extended syntax:
            case 'set', a, b:
                var[a] = value(b)
            case 'neq', a, b:
                var[a] = int(var[a] != value(b))

    return var


def to_python(instructions, i):
    """convert a set of instructions to Python code"""

    lines = [
        f'def f{i}(digit, z):'
    ]
    indent = ' '*4

    for instruction in instructions:
        match instruction:
            case 'inp', a:
                line = f"{a} = digit"
            case 'add', a, b:
                line = f"{a} += {b}"
            case 'mul', a, b:
                line = f"{a} *= {b}"
            case 'div', a, b:
                line = f"{a} //= {b}"
            case 'mod', a, b:
                line = f"{a} %= {b}"
            case 'eql', a, b:
                line = f"{a} = int({a} == {b})"
            # Extended syntax:
            case 'set', a, b:
                line = f"{a} = {b}"
            case 'neq', a, b:
                line = f"{a} = int({a} != {b})"

        lines.append(indent + line)

    lines.append(indent + 'return z')
    return "\n".join(lines) + '\n'

def to_fortran(instructions, i):
    """convert a set of instructions to Python code"""

    lines = [
        f'pure integer function f{i}(digit, inz)',
        'integer, intent(in) :: digit, inz',
        'integer :: w, x, y, z',
        '',
        'z = inz',
    ]
    indent = ' '*4

    for instruction in instructions:
        match instruction:
            case 'inp', a:
                line = f"{a} = digit"
            case 'add', a, b:
                line = f"{a} = {a} + {b}"
            case 'mul', a, b:
                line = f"{a} = {a} * {b}"
            case 'div', a, b:
                line = f"{a} = {a} / {b}"
            case 'mod', a, b:
                line = f"{a} = MOD({a}, {b})"
            case 'eql', a, b:
                line = f"{a} = {a} == {b}"
            # Extended syntax:
            case 'set', a, b:
                line = f"{a} = {b}"
            case 'neq', a, b:
                line = f"{a} = {a} /= {b}"

        lines.append(indent + line)
    lines.append(indent + f'f{i} = z')

    lines.append('end function')

    return "\n".join(lines) + '\n'

def optimize(instructions):
    result = []
    previous_instruction = None
    maybe_set = False
    maybe_neq = False
    for instruction in instructions:
        match instruction:
            case 'div', _, '1':
                maybe_set = False
                maybe_neq = False
            case 'mul', v, '0':
                maybe_set = v
                maybe_neq = False
            case 'add', a, b:
                if maybe_set == a:
                    result.append(('set', a, b))
                else:
                    # result.append(previous_instruction)
                    result.append(instruction)
                maybe_set = False
            case 'eql', a, '0':
                if maybe_neq and maybe_neq[0] == a:
                    result.append(('neq', *maybe_neq))
                else:
                    result.append(instruction)
                maybe_neq = False
            case 'eql', a, b:
                maybe_neq = (a, b)
            case _:
                if maybe_set or maybe_neq:
                    result.append(previous_instruction)
                maybe_set = False
                maybe_neq = False
                result.append(instruction)
        previous_instruction = instruction
    return tuple(result)


def inp_parts(instruction_str):
    parts = []
    for line in instruction_str.splitlines():
        line = line.strip()
        if line.startswith('inp'):
            part = []
            parts.append(part)
        part.append(tuple(line.split()))

    return tuple(tuple(part) for part in parts)


def verify_only_z(parts):
    # Check what we need to change in a part
    effects = []
    for part in parts:
        part_effects = set()
        for digit in VALID_DIGITS:
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
        assert part[1] == ('mul', 'x', '0')
        yreferenced = False
        for instruction in part:
            if instruction[-1] == 'y':
                yreferenced = True
            if instruction == ('mul', 'y', '0'):
                assert not yreferenced
                break
    print("Verified only using z")


def make_serial(parts, z, digits):
    first, *rest = parts

    level = 14 - len(parts)

    for digit in digits:
        if level == 0:
            print()
            print(digit, '- ', end='')
        if level == 1:
            print(digit, end='')

        key = (digit, z, level)
        if key in CACHE:
            return CACHE[key]

        outz = first(digit, z)

        # last part - check sum
        if not rest:
            if outz == 0:
                return [digit]
            else:
                continue

        remaining_serial = make_serial(rest, outz, digits)
        CACHE[key] = remaining_serial

        if not remaining_serial:
            continue

        return [digit] + remaining_serial


if __name__ == "__main__":
    do_fortran = False

    instruction_str = parse('input.txt')

    parts = inp_parts(instruction_str)

    verify_only_z(parts)

    parts = tuple(optimize(part) for part in parts)

    fnames = []
    for i, part in enumerate(parts):
        exec(compile(to_python(part, i), f'f{i}.py', 'exec'))
        fnames.append(f'f{i}')
    functions = eval(f'[{", ".join(fnames)}]')

    if do_fortran:
        from numpy import f2py

        fortran_code = '\n'.join(to_fortran(part, i) for i, part in enumerate(parts))
        f2py.compile(fortran_code, modulename='fortran_functions', extension='.f90')
        from fortran_functions import *

        functions = eval(f'[{", ".join(fnames)}]')

    # Caching the functions just makes them slower
    # functions = [cache(f) for f in functions]

    CACHE = {}

    part_1_serial = make_serial(functions, 0, VALID_DIGITS[::-1])
    print()
    solution(''.join(str(d) for d in part_1_serial))

    # Part 2
    # Scrub cached "working" values but retain knowledge about invalid combos
    CACHE = {key: value for key, value in CACHE.items() if not value}
    part_2_serial = make_serial(functions, 0, VALID_DIGITS)
    print()
    solution(''.join(str(d) for d in part_2_serial))