from collections import defaultdict
from functools import reduce

from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

digits_to_segments = {
    "0": "abcefg",
    "1": "cf",
    "2": "acdeg",
    "3": "acdfg",
    "4": "bcdf",
    "5": "abdfg",
    "6": "abdefg",
    "7": "acf",
    "8": "abcdefg",
    "9": "abcdfg",
}

pattern_to_digit = {value: key for key, value in digits_to_segments.items()}

# +
segment_to_digit = defaultdict(set)

for digit, segments in digits_to_segments.items():
    for segment in segments:
        segment_to_digit[segment].add(digit)


# -


def sortstring(s):
    return "".join(sorted(s))


with open(filename) as f:
    entries = [
        [[sortstring(s) for s in item.split()] for item in line.strip().split("|")]
        for line in f
    ]

easy_digits = ["1", "4", "7", "8"]

easy_lengths = {
    len(lit): digit for digit, lit in digits_to_segments.items() if digit in easy_digits
}

all_segments = "abcdefg"

# # Part 1

# +
count = 0

for unique_patterns, output_patterns in entries:
    for output_pattern in output_patterns:
        if len(output_pattern) in easy_lengths:
            count += 1

solution(count)


# -

# # Part 2


def decode(entry):
    unique_patterns, output_patterns = entry

    # Step 1: figure out possibe digits using the length like in part 1
    unique_pattern_to_digit = defaultdict(set)

    for digit, segment in digits_to_segments.items():
        for unique_pattern in unique_patterns:
            if len(segment) == len(unique_pattern):
                unique_pattern_to_digit[unique_pattern].add(digit)

    # Step 2: figure out from logic which possible wire-segment connections there are
    possible_wire_to_segment = {wire: set(all_segments) for wire in all_segments}

    for unique_pattern, possible_digits in unique_pattern_to_digit.items():
        definitely_dark_wires = set(all_segments)
        possible_lit_wires = []

        for digit in possible_digits:
            digit_lit_wires = set(digits_to_segments[digit])
            definitely_dark_wires -= digit_lit_wires
            possible_lit_wires.append(digit_lit_wires)

        definitely_lit_wires = reduce(set.intersection, possible_lit_wires)

        for dark_wire in definitely_dark_wires:
            for lit_segment in set(unique_pattern):
                possible_wire_to_segment[dark_wire] -= {lit_segment}

        for dark_segment in set(all_segments) - set(unique_pattern):
            for lit_wire in definitely_lit_wires:
                possible_wire_to_segment[lit_wire] -= {dark_segment}

    # Step 3: propagate known connections through candidate lists
    while True:
        for wire, possibles in possible_wire_to_segment.items():
            if len(possibles) == 1:
                for otherwire in possible_wire_to_segment:
                    if wire != otherwire:
                        possible_wire_to_segment[otherwire] -= possibles

        if all(len(possibles) == 1 for possibles in possible_wire_to_segment.values()):
            break

    # Now we know the wire-segment mapping
    actual_segment_to_wire = {
        segment: wire for wire, [segment] in possible_wire_to_segment.items()
    }

    def real_digit(pattern):
        return pattern_to_digit[
            "".join(sorted(actual_segment_to_wire[c] for c in pattern))
        ]

    output_digits = "".join(real_digit(output) for output in output_patterns)

    output_value = int(output_digits)

    return output_value


all_numbers = [decode(entry) for entry in entries]

solution(sum(all_numbers))
