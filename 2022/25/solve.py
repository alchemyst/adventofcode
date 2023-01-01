from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

numbers = []
with open(filename) as f:
    for line in f:
        numbers.append(line.strip())


def unsnafu(s):
    digits = []
    for c in s:
        if c in '012':
            n = int(c)
        elif c == '-':
            n = -1
        elif c == '=':
            n = -2
        else:
            print("Unexpected digit!", c)
        digits.append(n)

    return sum(n * 5 ** p for p, n in enumerate(reversed(digits), 0))


def conv_base(n, base):
    digits = []
    d = 0
    while n > 0:
        n, d = divmod(n, base)
        digits.insert(0, d)
    return digits


def snafu(digits):
    carry = 0
    chars = []
    for p, n in enumerate(reversed(digits)):
        carry, d = divmod(n + carry, 5)
        if d in {0, 1, 2}:
            c = str(d)
        elif d == 3:
            c = '='
            carry += 1
        elif d == 4:
            c = '-'
            carry += 1
        chars.append(c)
    if carry > 0:
        chars.append(str(carry))
    return ''.join(reversed(chars))


tests = [
    [1, '1'],
    [2, '2'],
    [3, '1='],
    [4, '1-'],
    [5, '10'],
    [6, '11'],
    [7, '12'],
    [8, '2='],
    [9, '2-'],
    [10, '20'],
    [15, '1=0'],
    [20, '1-0'],
    [2022, '1=11-2'],
    [12345, '1-0---0'],
    [314159265, '121-1110-1=0'],
]

if debug:
    for v, s in tests:
        converted = snafu(conv_base(v, 5))
        print(f"{v:10} {s:10s} {converted:10} {unsnafu(converted)}")

# Part 1
total = 0
for digits in numbers:
    value = unsnafu(digits)
    # print(value)
    total += value

solution(snafu(conv_base(total, 5)))

# Part 2
solution('Dummy')
