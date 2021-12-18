import itertools
import math
import re
from aoc import solution

tokenre = re.compile(r'(,|\[|\]|[0-9]+)')
superdebug = False
debug = False


def parse_ints(l):
    return [int(i) if i.isdigit() else i for i in l]


def parse_line(line):
    return parse_ints(tokenre.findall(line.strip()))


def parse(filename):
    with open(filename) as f:
        numbers = [parse_line(line.strip()) for line in f if line.strip()]
    return numbers


def parse_example(string):
    return [parse_line(line.strip()) for line in string.split('\n') if line.strip()]


def display(number):
    return ''.join(str(i) for i in number)


def explode(number):
    levels = 0

    for i, c in enumerate(number):
        if c == '[':
            levels += 1
            continue
        if c == ']':
            levels -= 1
            continue
        if c == ',':
            continue

        # This has to be a number
        if levels == 5:  # explode
            reduced_number = number.copy()

            if superdebug: print('Explode')
            left_value = c
            right_value = number[i + 2]
            # scan left
            ii = i - 1
            while ii >= 0:
                if isinstance(reduced_number[ii], int):
                    reduced_number[ii] += left_value
                    break
                ii -= 1
            # scan right - skip comma and number
            ii = i + 3
            while ii < len(reduced_number):
                if isinstance(reduced_number[ii], int):
                    reduced_number[ii] += right_value
                    break
                ii += 1

            # replace with 0
            reduced_number[i - 1:i + 4] = [0]

            # Done processing
            return True, reduced_number
    else:
        return False, number


def split(number):
    reduced_number = number.copy()
    for i, c in enumerate(number):
        if c == '[':
            continue
        if c == ']':
            continue
        if c == ',':
            continue
        if c >= 10:
            if superdebug: print('Split')
            left_value = int(math.floor(c / 2))  # rounded down
            right_value = int(math.ceil(c / 2))  # rounded up

            newpair = ['[', left_value, ',', right_value, ']']
            reduced_number[i:i + 1] = newpair

            return True, reduced_number
    else:
        return False, number


def reduce(number):
    if superdebug: print('Called with', display(number))
    levels = 0

    exploded, new_number = explode(number)
    if exploded:
        return reduce(new_number)

    splitted, new_number = split(number)
    if splitted:
        return reduce(new_number)

    return number


def add(left, right):
    result = reduce(['[', *left, ',', *right, ']'])

    # print('  ', display(left))
    # print(' +', display(right))
    # print(' =', display(result))
    # print('')

    return result


def add_all(numbers):
    a, b, *rest = numbers
    result = add(a, b)
    for c in rest:
        result = add(result, c)

    return result


def magnitude(number):
    def _magnitude(nested_number):
        if isinstance(nested_number, int):
            return nested_number
        left, right = map(_magnitude, nested_number)
        return 3*left + 2*right
    return _magnitude(eval(display(number)))


def check_example(example, solution):
    assert display(add_all(parse_example(example))) == solution
    print('Correct!')
    print("")


if __name__ == '__main__':
    filename = 'test.txt' if debug else 'input.txt'

    numbers = parse(filename)
    result = add_all(numbers)
    solution(magnitude(result))

    biggest = 0

    for a, b in itertools.product(numbers, repeat=2):
        if a == b:
            continue
        for swap in (True, False):
            result = add(b, a) if swap else add(a, b)
            mag = magnitude(result)
            if mag > biggest:
                biggest = mag

    solution(biggest)