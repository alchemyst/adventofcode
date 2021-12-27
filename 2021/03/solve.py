import numpy as np
from collections  import Counter

from aoc import solution

debug = False
with open('input.txt') as f:
    data = [line.strip() for line in f]

darr = np.array(list(map(list, data)))

gamma_bits = []
epsilon_bits = []

for position in range(darr.shape[1]):
    counts = Counter(darr[:, position]).most_common()
    most_common_bit = counts[0][0]
    least_common_bit = counts[-1][0]
    gamma_bits.append(most_common_bit)
    epsilon_bits.append(least_common_bit)


gamma_rate = int(''.join(gamma_bits), base=2)
epsilon_rate = int(''.join(epsilon_bits), base=2)
power_consumption = gamma_rate * epsilon_rate

solution(power_consumption)


# Part 2

def bitcount(it):
    count = {'0': 0, '1': 0}

    for i in it:
        count[i] += 1

    if count['0'] > count['1']:
        return '0', '1', False
    if count['1'] > count['0']:
        return '1', '0', False
    return '0', '1', True


def apply_bit_criteria(data, hi, position):
    most_common_bit, least_common_bit, same = bitcount([line[position] for line in data])

    if hi:
        bitvalue = '1' if same else most_common_bit
    else:
        bitvalue = '0' if same else least_common_bit

    newdata = [line for line in data if line[position] == bitvalue]

    return bitvalue, newdata
    

def bitcheck(data, hi):
    runningdata = data.copy()

    for position in range(darr.shape[1]):
        bitvalue, runningdata = apply_bit_criteria(runningdata, hi, position)
        if debug: print(bitvalue, runningdata)
        if len(runningdata) <= 1:
            break
    return runningdata[0]


oxygen_generator_rating = int(bitcheck(data, True), base=2)
CO2_scrubber_rating = int(bitcheck(data, False), base=2)

solution(oxygen_generator_rating*CO2_scrubber_rating)

