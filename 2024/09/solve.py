import itertools

import more_itertools

from aoc import solution
import pathlib

debug = False
filename = 'test.txt' if debug else 'input.txt'

def read_diskmap(filename):
    diskmap = []
    numbers = [int(c) for c in pathlib.Path(filename).read_text().strip()]
    spaces = []
    files = []
    for file_id, maybe_pair in enumerate(more_itertools.batched(numbers, 2)):
        if len(maybe_pair) == 1:
            file_space, free_space = maybe_pair[0], 0
        else:
            file_space, free_space = maybe_pair

        files.append((file_id, len(diskmap), file_space))

        if free_space > 0:
            spaces.append((len(diskmap) + file_space, free_space))

        diskmap.extend([file_id]*file_space + [None]*free_space)

    return diskmap, spaces, files

def diskmap_str(diskmap):
    return ''.join(str(file_id) if file_id is not None else '.' for file_id in diskmap)

# Part 1
diskmap, _, _ = read_diskmap(filename)

first_empty = diskmap.index(None)
back = len(diskmap) - 1
while diskmap[back] is None:
    back -= 1

while first_empty < back:
    diskmap[first_empty], diskmap[back] = diskmap[back], diskmap[first_empty]
    while diskmap[first_empty] is not None:
        first_empty += 1
    while diskmap[back] is None:
        back -= 1

    if debug:
        print(diskmap_str(diskmap))

def checksum(diskmap):
    return sum(file_id*position for position, file_id in enumerate(diskmap) if file_id is not None)

solution(checksum(diskmap))

# Part 2
diskmap, spaces, files = read_diskmap(filename)

for file_id, file_position, file_space in reversed(files):
    # find space for file
    if debug:
        print(file_id)
    for space_index, (space_position, space_size) in enumerate(spaces):
        if space_size >= file_space:
            break
    else:
        continue

    # only move files left
    if space_position >= file_position:
        continue

    # Move file to space
    diskmap[file_position : file_position + file_space] = [None]*file_space
    diskmap[space_position : space_position + file_space] = [file_id]*file_space

    # Update spaces
    spaces[space_index] = (space_position + file_space, space_size - file_space)
    spaces.append((file_position, file_space))
    spaces.sort()

    # combine adjacent spaces
    while True:
        for space_index, ((left_position, left_size), (right_position, right_size)) in enumerate(itertools.pairwise(spaces)):
            if left_position + left_size == right_position:
                spaces[space_index] = (left_position, left_size + right_size)
                spaces.pop(space_index + 1)
                break
        else:
            break

    if debug:
        print(diskmap_str(diskmap))


solution(checksum(diskmap))