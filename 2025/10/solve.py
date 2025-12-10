from aoc import solution, sum_every
from dataclasses import dataclass

debug = False
filename = "test.txt" if debug else "input.txt"


@dataclass
class Problem:
    target: tuple[bool, ...]
    buttons: tuple[tuple[int, ...], ...]
    joltage: tuple[int, ...]

    @classmethod
    def from_line(cls, line):
        machine_, *buttons_, joltage_ = line.strip().split()

        return cls(
            target=tuple(c == "#" for c in machine_[1:-1]),
            buttons=tuple(tuple(map(int, b[1:-1].split(","))) for b in buttons_),
            joltage=tuple(map(int, joltage_[1:-1].split(","))),
        )

    def start(self):
        return tuple(False for _ in self.target)


with open(filename) as f:
    problems = [Problem.from_line(line) for line in f]


# Part 1
def apply(button, state):
    return tuple(s ^ (i in button) for i, s in enumerate(state))


def search(start, target, buttons):
    queue = [start]
    seen = {start}
    steps = {start: 0}

    while queue:
        state = queue.pop(0)
        if state == target:
            return steps[state]
        for button in buttons:
            new_state = apply(button, state)
            if new_state in seen:
                continue

            seen.add(new_state)
            steps[new_state] = steps[state] + 1
            queue.append(new_state)


solution(sum(search(p.start(), p.target, p.buttons) for p in problems))

# Part 2

import scipy.optimize as opt


def min_presses(p: Problem) -> int:
    # solve as an milp
    # solution vector x: number of presses of each button
    # objective: minimize sum(x)
    # subject to
    # Ax = b
    # b is joltage
    # A[i][j] = 1 if i in buttons[j] else 0
    # integer constraints

    A = [
        [1 if i in button else 0 for button in p.buttons] for i in range(len(p.joltage))
    ]
    res = opt.linprog(
        c=[1] * len(p.buttons),
        A_eq=A,
        b_eq=(list(p.joltage)),
        bounds=[(0, None)] * len(p.buttons),
        method="highs",
        integrality=1,
    )

    return res.fun


for p in problems:
    print(min_presses(p))

solution(sum_every(min_presses, problems))
