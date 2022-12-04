from dataclasses import dataclass
from operator import attrgetter
import pprint

from aoc import solution
import re

debug = False
filename = 'test.txt' if debug else 'input.txt'
length = 1000 if debug else 2503

@dataclass
class Reindeer:
    name: str
    speed: int
    go_time: int
    rest_time: int
    timer: int = 0
    distance: int = 0
    state: str = "travelling"
    score: int = 0

    def advance(self, seconds=1):
        self.timer += seconds
        if self.state == "travelling":
            self.distance += self.speed*seconds

            self.state_check(self.go_time, "resting")
        elif self.state == "resting":
            self.state_check(self.rest_time, "travelling")

    def state_check(self, time, otherstate):
        if self.timer >= time:
            self.state = otherstate
            self.timer = 0

    def reset(self):
        self.state = "travelling"
        self.distance = 0
        self.timer = 0


spec = re.compile('([^ ]+)[^\d]*' + '(\d+)[^\d]*'*3)
reindeer = []
with open(filename) as f:
    for line in f:
        m = spec.match(line)
        name, *numbers = m.groups()

        speed, go_time, rest_time = map(int, numbers)

        reindeer.append(Reindeer(name, speed, go_time, rest_time))

# Part 1
for second in range(length):
    for r in reindeer:
        r.advance()

winner = max(reindeer, key=attrgetter('distance'))
solution(winner.distance)

# Part 2
for r in reindeer:
    r.reset()

for second in range(length):
    for r in reindeer:
        r.advance()
    winner = max(reindeer, key=attrgetter('distance'))
    for r2 in reindeer:
        if r2.distance == winner.distance:
            r2.score += 1

winner = max(reindeer, key=attrgetter('score'))
solution(winner.score)