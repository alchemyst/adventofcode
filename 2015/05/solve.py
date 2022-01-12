import re
from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.readlines()


def pairwise(s):
    """
    s is a string
    return a list of pairs of characters
    """
    return zip(s[:-1], s[1:])


def nice1(s):
    """
    A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

    :param s:
    :return:
    """
    vowels = "aeiou"
    bad_strings = ["ab", "cd", "pq", "xy"]

    nvowels = sum(s.count(v) for v in vowels)
    if nvowels < 3:
        return False

    for pair in pairwise(s):
        if pair[0] == pair[1]:
            break
    else:
        return False

    if any(x in s for x in bad_strings):
        return False

    return True

# Part 1
nice_strings = [s for s in lines if nice1(s)]
solution(len(nice_strings))

# Part 2
repeated = re.compile(r'(..).*\1')
repeated_with_one = re.compile(r'(.).\1')
nice_strings = [s for s in lines if repeated.search(s) and repeated_with_one.search(s)]
solution(len(nice_strings))