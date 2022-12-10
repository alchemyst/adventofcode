from aoc import solution, print_board
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'


class CPU:
    def __init__(self):
        self.cycle = 1
        self.x = 1
        self.history = []
        self.cycles = []

    def tick(self):
        self.history.append(self.x)
        self.cycles.append(self.cycle)
        self.cycle += 1

    def noop(self):
        self.tick()

    def addx(self, ax):
        for _ in range(2):
            self.tick()
        self.x += ax

    def signalstrength(self):
        r = 0
        for c, s in zip(self.cycles[19::40], self.history[19::40]):
            if debug: print(c, s, c*s)
            r += c*s
        return r

    def printhistory(self):
        for c, s in zip(self.cycles, self.history):
            print(c, s)


cpu = CPU()
with open(filename) as f:
    for line in f:
        match line.strip().split():
            case ["noop"]:
                cpu.noop()
            case ['addx', ax_str]:
                ax = int(ax_str)
                cpu.addx(ax)

# Part 1
solution(cpu.signalstrength())

cycle_map = (np.reshape(np.array(cpu.cycles), (len(cpu.cycles)//40, 40)) - 1) % 40
x_map = np.reshape(np.array(cpu.history), (len(cpu.cycles)//40, 40))
pixels = np.abs(x_map - cycle_map) <= 1
print_board(pixels, lookup='.#', type='s')

# Part 2
solution('Dummy')