from statistics import median

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = [line.strip() for line in f]

line = lines[0]

opening = "([{<"
closing = ")]}>"

corrupt_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
complete_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

corrupt_score = 0
complete_scores = []

for line in lines:
    stack = []
    for char in line:
        if char in opening:
            stack.append(char)
            continue

        openchar = stack.pop()
        correct_closing = closing[opening.index(openchar)]
        if char != correct_closing:   # corrupted line
            if debug:
                print("Incorrect closing:", char)
            corrupt_score += corrupt_points[char]
            break
    else:  # incomplete line
        completion = ''.join(closing[opening.index(openchar)] for openchar in reversed(stack))
        score = 0
        for char in completion:
            score = score*5 + complete_points[char]

        if debug:
            print('Incomplete line, completion:', completion, score)

        complete_scores.append(score)


print("Part 1:", score)

print("Part 2:", median(complete_scores))