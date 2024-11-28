from aoc import solution
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

property_names = ["capacity", "durability", "flavor", "texture", "calories"]

value_matrix = []

with open(filename) as f:
    for line in f.read().splitlines(keepends=False):
        ingredient, properties = line.split(': ')
        values = []
        for pair in properties.split(', '):
            property, value = pair.split()
            value = int(value)
            values.append(value)
        value_matrix.append(values)

value_matrix = np.array(value_matrix)

value_matrix, calorie_vector = value_matrix[:, :4], value_matrix[:, 4]
# Part 1
def value(recipe):
    return np.prod(np.maximum(0, recipe @ value_matrix))

total = 100

def combos(given, length):

    used = sum(given)
    remaining  = total - used

    if len(given) == length - 1:
        yield [*given, remaining]
        return

    for this in range(remaining + 1):
        yield from combos([*given, this], length)

best_recipe_value = max((value(c) for c in combos([], len(value_matrix))))

solution(best_recipe_value)

# Part 2
def calories(recipe):
    return recipe @ calorie_vector

best_recipe_value = max((value(c) for c in combos([], len(value_matrix)) if calories(c) == 500))

solution(best_recipe_value)