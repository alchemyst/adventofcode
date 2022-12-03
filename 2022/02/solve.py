from aoc import solution

"""
"""


debug = False
filename = 'test.txt' if debug else 'input.txt'


beats = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock',
}

loses = {b: a for a, b in beats.items()}

mapping1 = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
}

mapping2 = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors',
}

outcome_scores = {
    'win': 6,
    'draw': 3,
    'lose': 0,
}

shape_scores = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
}


def score(play1, play2):
    if play1 == play2:
        outcome = 'draw'
    elif beats[play1] == play2:
        outcome = 'win'
    else:
        outcome = 'lose'

    return outcome_scores[outcome] + shape_scores[play2]


def evaluate1(code1, code2):
    play1 = mapping1[code1]
    play2 = mapping2[code2]

    return score(play1, play2)


def evaluate2(code1, code2):
    play1 = mapping1[code1]
    if code2 == 'X':
        play2 = loses[play1]
    elif code2 == 'Y':
        play2 = play1
    elif code2 == 'Z':
        play2 = beats[play1]

    return score(play1, play2)


def run(plays, evaluate):
    return sum(evaluate(code1, code2) for code1, code2 in plays)


plays = []

with open(filename) as f:
    for line in f:
        plays.append(line.strip().split())


# Part 1
solution(run(plays, evaluate1))

# Part 2
solution(run(plays, evaluate2))