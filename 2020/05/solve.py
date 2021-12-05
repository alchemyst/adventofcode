#!/usr/bin/env python

def partition(str, length, lower, upper):
    values = list(range(length))

    for direction in str:
        midpoint = int(len(values) // 2)
        if direction == lower:
            values = values[:midpoint]
        if direction == upper:
            values = values[midpoint:]

    return values[0]

# FBFBBFFRLR

def seat_id(string):
    row = partition(string[:7], 128, 'F', 'B')
    seat = partition(string[7:], 8, 'L', 'R')

    return row*8 + seat

print(seat_id('FBFBBFFRLR'))
ids = []
with open('05/input.txt') as f:
    for line in f:
        line.strip()
        ids.append(seat_id(line))

print(max(ids))

for i in range(max(ids)):
    if i not in ids and i-1 in ids and i+1 in ids:
        print(i)