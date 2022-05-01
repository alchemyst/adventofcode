from itertools import groupby

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    line = f.read().strip()

badletters = set("iol")

def increment(string):
    position = len(string) - 1
    carry = 1

    lst = list(string)

    while carry:
        if lst[position] == 'z':
            lst[position] = 'a'
            carry = 1
            position -= 1
            if position < 0:
                position = len(string) - 1
                carry = 0
        else:
            lst[position] = chr(ord(lst[position]) + 1)
            carry = 0
            if lst[position] in badletters:
                carry = 1

    return ''.join(lst)

assert increment("az") == "ba"
assert increment("zz") == "aa"

def has_straight(string):
    start = True
    for c1, c2 in zip(string, string[1:]):
        if start:
            count = 1
            start = False
        if ord(c1) + 1 == ord(c2):
            count += 1
        else:
            start = True

        if count >= 3:
            return True

    return False

assert has_straight("abc")

def has_pairs(string):
    pair_chars = set()
    for c, group in groupby(string):
        if len(list(group)) >= 2:
            pair_chars.add(c)

    return len(pair_chars) >= 2

assert has_pairs("aabb")
assert not has_pairs("abcdd")
assert not has_pairs("aabaa")

def valid(password):
    return (
        has_straight(password)
        and badletters.isdisjoint(password)
        and has_pairs(password)
    )

assert not valid("hijklmmn")
assert not valid("abbceffg")
assert not valid("abbcegjk")

def nextpassword(password):
    # fast forward to next after bad letters
    for i, c in enumerate(password):
        if c in badletters:
            password = password[:i+1] + 'z'*(len(password) - i - 1)
            break

    while True:
        password = increment(password)
        if valid(password):
            break

    return password

assert nextpassword("abcdefgh") == "abcdffaa"
assert nextpassword("ghijklmn") == "ghjaabcc"


# Part 1
p = nextpassword(line)
solution(p)

# Part 2
solution(nextpassword(p))
