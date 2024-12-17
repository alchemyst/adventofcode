from dataclasses import dataclass, field
from itertools import count
import scipy.optimize as sco

from aoc import solution
from aoc.parse import all_numbers
debug = False
filename = 'test.txt' if debug else 'input.txt'

instruction_names = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]

@dataclass
class Machine:
    a: int
    b: int
    c: int
    program: list[int]
    ip: int = 0
    output: list[int] = field(default_factory=list)

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            registers, program_line = f.read().split('\n\n')

        return cls(*all_numbers(registers), all_numbers(program_line))

    def combo(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            raise ValueError(f'Invalid operand {operand}')

    def step(self):
        if self.ip >= len(self.program):
            return False

        opcode = self.program[self.ip]
        instruction = instruction_names[opcode]
        operand = self.program[self.ip + 1]

        jump = False
        match instruction:
            case "adv":
                self.a = self.a // 2**self.combo(operand)
            case "bdv":
                self.b = self.a // 2**self.combo(operand)
            case "cdv":
                self.c = self.a // 2**self.combo(operand)
            case "bxl":
                self.b = self.b ^ operand
            case "bst":
                self.b = self.combo(operand) % 8
            case "jnz":
                if self.a != 0:
                    self.ip = operand
                    jump = True
            case "bxc":
                self.b = self.b ^ self.c
            case "out":
                self.output.append(self.combo(operand) % 8)
        if not jump:
            self.ip += 2

        return True

    def run(self):
        while self.step():
            pass

        return ",".join(str(i) for i in self.output)

    def run_checking_output(self, target):
        while self.step():
            if self.output != target[:len(self.output)]:
                return False

        return self.output == target


# Part 1
machine = Machine.from_file(filename)
output = machine.run()

solution(output)

# Part 2
base_machine = Machine.from_file(filename)

def run_with(i):
    machine = Machine(base_machine.a, base_machine.b, base_machine.c, base_machine.program)
    machine.a = i

    machine.run()

    return machine


# bisect to find the first time the output is the same length
left  = 30000000000000
right = 600000000000000
len_target = len(base_machine.program)

while True:
    midpoint = (left + right) // 2
    len_left = len(run_with(left).output)
    len_right = len(run_with(right).output)
    len_midpoint = len(run_with(midpoint).output)

    if len_midpoint >= len_target:
        right = midpoint
    else:
        left = midpoint

    if left == right - 1:
        break

register_a = right

while True:
    output = run_with(register_a).output
    if tuple(output) == base_machine.program:
        break

    # Skip forward past the repeats
    for position in reversed(range(len_target)):
        if output[position] != base_machine.program[position]:
            break
    register_a += 8**position

solution(register_a)