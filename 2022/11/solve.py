import heapq
import numpy as np
from more_itertools import chunked

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'


class World:
    def __init__(self, divide_by_three):
        self.worry_levels = []
        self.monkeys = []
        self.divide_by_three = divide_by_three
        self.modulus = 1

    def add_worry(self, worry_level):
        r = len(self.worry_levels)
        self.worry_levels.append(worry_level)
        return r

    def read_monkeys(self, f):
        self.monkeys = [
            Monkey(chunk, self)
            for chunk in chunked(f.read().splitlines(), 7)
        ]

        alldivisors = [monkey.divisor for monkey in self.monkeys]
        self.modulus = np.prod(alldivisors)

    def manage(self, worry_level):
        if self.divide_by_three:
            worry_level //= 3
        else:
            worry_level %= self.modulus

        return worry_level


class Monkey:
    def __init__(self, lines, world):
        self.inspections = 0
        self.world = world
        self.number = int(lines[0].split()[-1][:-1])

        worry_levels = [int(item) for item in lines[1].split(':')[1].strip().split(', ')]
        self.items = [self.world.add_worry(worry_level) for worry_level in worry_levels]

        self.operation = lines[2].split(':')[1].strip().split(' = ')[-1]
        self.divisor = int(lines[3].split()[-1])
        self.targets = [int(l.split()[-1]) for l in lines[4:6]][::-1]

    def inspect(self, item):
        self.inspections += 1
        worry_level = self.world.worry_levels[item]
        worry_level = eval(self.operation, {'old': worry_level})

        worry_level = self.world.manage(worry_level)

        self.world.worry_levels[item] = worry_level

        target = self.targets[int(worry_level % self.divisor == 0)]

        return target

    def turn(self):
        for item in self.items:
            target = self.inspect(item)
            self.world.monkeys[target].items.append(item)
        self.items = []

    def print_worry(self):
        worries = [self.world.worry_levels[item] for item in self.items]
        print(f'Monkey {self.number}: worry: {worries}, inspected: {self.inspections}')


def run_game(divide_by_three, rounds, print_interval=1):
    world = World(divide_by_three)

    with open(filename) as f:
        world.read_monkeys(f)

    if debug:
        print(world.monkeys)
        for monkey in world.monkeys:
            monkey.print_worry()

    for i in range(rounds):
        for monkey in world.monkeys:
            monkey.turn()
        if debug and (i+1) % print_interval == 0:
            print('After round', i+1)
            for monkey in world.monkeys:
                monkey.print_worry()
            print()

    m1, m2 = heapq.nlargest(2, world.monkeys, key=lambda m: m.inspections)
    monkey_business = m1.inspections * m2.inspections

    return monkey_business


# Part 1
solution(run_game(divide_by_three=True, rounds=20))

# Part 2
solution(run_game(divide_by_three=False, rounds=10000, print_interval=1000))