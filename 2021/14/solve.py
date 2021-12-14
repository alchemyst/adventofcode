from collections import Counter

debug = False
filename = 'test.txt' if debug else 'input.txt'


def pairwise(iterable):
    return zip(iterable, iterable[1:])

def parse(filename):
    with open(filename) as f:
        template = next(f).strip()
        next(f)
        rules = dict(line.strip().split(' -> ') for line in f)
    return template, rules

# I implemented the basic string-based rules first,
# then used that to debug the pairwise implementation

def polymerize(polymer):
    newpolymer = []
    for a, b in pairwise(polymer):
        s = a+b
        newpolymer.append(a)
        if s in rules:
            newpolymer.append(rules[s])
    newpolymer.append(b)
    return ''.join(newpolymer)


def pair_polymerize(pairs):
    newpairs = Counter()
    for pair, count in pairs.items():
        if pair in pair_rules:
            a, b = pair
            i = pair_rules[pair]
            newpairs[(a, i)] += count
            newpairs[(i, b)] += count
        else:
            newpairs[pair] = count
    return newpairs


template, rules = parse(filename)

polymer = template
# print("Template:        ", polymer)
for i in range(10):
    step = i + 1
    polymer = polymerize(polymer)
    # print(F"After step {step}: ", polymer)

count = Counter(polymer)
if debug:
    print(count)
print('Part 1:', max(count.values()) - min(count.values()))


# Part 2

# Clearly we need to be more efficient in storing thes things - just store pairs
pairs = Counter(pairwise(template))
pair_rules = {tuple(rule): value for rule, value in rules.items()}

# Polymerize
newpairs = pairs.copy()
for i in range(40):
    newpairs = pair_polymerize(newpairs)

# Count
newcounts = Counter()
for (a, _), count in newpairs.items():
    newcounts[a] += count
# Tricky - you have to add the last item,
# which will never change because you're always adding in the middle of two
newcounts[template[-1]] += 1

print('Part 2:', max(newcounts.values()) - min(newcounts.values()))
