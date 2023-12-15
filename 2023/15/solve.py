from collections import defaultdict, deque
from functools import cache

from aoc import solution, sum_every

debug = False
filename = 'test.txt' if debug else 'input.txt'

@cache
def hash_string(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value


assert hash_string('HASH') == 52

with open(filename) as f:
    line = f.read().strip()

instructions = line.split(',')

# Part 1
solution(sum_every(hash_string, instructions))

# Part 2
n_boxes = 256

# Front of box is 0, back of box is end
boxes = [[] for _ in range(n_boxes)]
lens_locations = [{} for _ in range(n_boxes)]  # [box_index](label) -> (slot_index)

for instruction in instructions:
    if instruction.endswith('-'):
        label = instruction[:-1]
        box_index = hash_string(label)
        lens_location_by_label = lens_locations[box_index]
        if label in lens_location_by_label:
            slot_index = lens_location_by_label[label]
            del boxes[box_index][slot_index]
            del lens_location_by_label[label]
            for other_label, other_slot_index in lens_location_by_label.items():
                if other_slot_index > slot_index:
                    lens_location_by_label[other_label] -= 1

    elif '=' in instruction:
        label, focal_length = instruction.split('=')
        focal_length = int(focal_length)

        box_index = hash_string(label)

        box = boxes[box_index]
        lens_location_by_label = lens_locations[box_index]

        if label in lens_location_by_label:
            box[lens_location_by_label[label]] = focal_length
        else:
            box.append(focal_length)
            lens_location_by_label[label] = len(box) - 1

    else:
        raise ValueError(f'Invalid instruction {instruction}')


    if debug:
        print(f"After {instruction}")
        # print(lens_locations)
        for box_index in range(n_boxes):
            if boxes[box_index]:
                print(f"Box {box_index}:", end=' ')
                for label, slot_index in sorted(lens_locations[box_index].items(), key=lambda x: x[1]):
                    print(f"[{slot_index} {label} {boxes[box_index][slot_index]}]", end=' ')
                print()
        print()

total = 0
for box_index, (box, lens_location_by_label) in enumerate(zip(boxes, lens_locations)):
    for label, slot_index in lens_location_by_label.items():
        power = (box_index + 1) * (slot_index + 1) * box[slot_index]
        total += power

solution(total)
