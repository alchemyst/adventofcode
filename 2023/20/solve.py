import math

from collections import defaultdict, Counter

import numpy as np

from aoc import solution

debug = False
filename = 'test2.txt' if debug else 'input.txt'

class Module:
    def __init__(self, name, upstream, downstream):
        self.name = name
        self.upstream = upstream
        self.downstream = downstream

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.upstream}, {self.downstream})'

    def handle(self, source, pulse):
        return []

class Broadcaster(Module):
    def handle(self, source, pulse):
        for downstream in self.downstream:
            yield self.name, pulse, downstream


class FlipFlop(Module):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially
    off. If a flip-flop module receives a high pulse, it is ignored and
    nothing happens. However, if a flip-flop module receives a low
    pulse, it flips between on and off. If it was off, it turns on and
    sends a high pulse. If it was on, it turns off and sends a low
    pulse.
    """
    def __init__(self, name, upstream, downstream):
        super().__init__(name, upstream, downstream)
        self.state = False  # "off"

    def handle(self, source, pulse):
        match pulse:
            case 'high':
                return []
            case 'low':
                self.state = not self.state
                send_pulse = 'high' if self.state else 'low'
                return [(self.name, send_pulse, downstream) for downstream in self.downstream]


class Conjunction(Module):
    """
    Conjunction modules (prefix &) remember the type of the most recent
    pulse received from each of their connected input modules; they
    initially default to remembering a low pulse for each input. When
    a pulse is received, the conjunction module first updates its memory
    for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    """
    def __init__(self, name, upstream, downstream):
        super().__init__(name, upstream, downstream)
        self.memory = defaultdict(lambda: 'low')

    def handle(self, source, pulse):
        self.memory[source] = pulse
        if all(self.memory[input] == 'high' for input in self.upstream):
            sent_pulse = 'low'
        else:
            sent_pulse = 'high'

        return [(self.name, sent_pulse, downstream) for downstream in self.downstream]


def build_network(filename):
    modules = {}
    upstream = defaultdict(list)

    with open(filename) as f:
        for line in f.read().splitlines(keepends=False):
            code_name, connections_list = line.split(' -> ')
            downstream_modules = connections_list.split(', ')

            if code_name == 'broadcaster':
                name = code_name
                constructor = Broadcaster
            elif code_name.startswith('%'):
                name = code_name[1:]
                constructor = FlipFlop
            elif code_name.startswith('&'):
                name = code_name[1:]
                constructor = Conjunction
            else:
                name = code_name
                constructor = Module

            modules[name] = constructor(name, upstream[name], downstream_modules)

            for downstream in downstream_modules:
                upstream[downstream].append(name)

    for module in list(modules.values()):
        for downstream in module.downstream:
            if downstream not in modules:
                modules[downstream] = Module(downstream, upstream[downstream], [])

    return modules, upstream


def push_button(modules):
    pulses = [('button', 'low', 'broadcaster')]
    counts = Counter()
    while pulses:
        source, pulse, target = pulses.pop(0)
        counts[pulse] += 1
        pulses += modules[target].handle(source, pulse)

    return counts

# Part 1
modules, upstream = build_network(filename)

counts = Counter()
for i in range(1000):
    counts += push_button(modules)

solution(counts['low']*counts['high'])

# Part 2
# This assumption is not super general - I noticed the upstream unit of rx is a conjunction
# then reasoned that the output will be low when all the conjunction outputs go high at the same time, from being low
# I spotted that this will be an lcm application, so looked for cycles
watch_nodes = set(upstream[upstream['rx'][0]])

cycles = defaultdict(list)
# give it a while for the cycles to be apparent
for i in range(1, 15000):
    pulses = [('button', 'low', 'broadcaster')]

    while pulses:
        source, pulse, target = pulses.pop(0)
        if target in watch_nodes:
            cycles[target].append((i, 0 if pulse == 'low' else 1))

        pulses += modules[target].handle(source, pulse)

periods = []
for name, cycle in cycles.items():
    a = np.array(cycle)
    period = np.unique(np.diff(a[a[:, 1] == 0, 0]))
    assert len(period) == 1

    periods.append(period[0])

solution(math.lcm(*periods))
