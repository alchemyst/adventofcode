from dataclasses import dataclass

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    numbers = [int(line.strip()) for line in f]


@dataclass
class ListItem:
    value: int
    previous: "ListItem"
    next: "ListItem"


def create_circle(numbers):
    circle = {}

    for index, number in enumerate(numbers):
        circle[index] = ListItem(number, None, None)
        if number == 0:
            zero = circle[index]

    for index, item in circle.items():
        if index < len(circle)-1:
            item.next = circle[index+1]
        if index > 0:
            item.previous = circle[index-1]

    # hook up last item to first item
    circle[len(circle)-1].next = circle[0]
    # hook up first item to last item
    circle[0].previous = circle[len(circle)-1]

    return zero, circle

def print_array(circle):
    item = circle[0]
    items = [item.value]
    for _ in range(len(circle) - 1):
        item = item.next
        items.append(item.value)

    print(items)
    print()

    # item = circle[0]
    # items = []
    # for _ in range(len(circle) - 1):
    #     item = item.previous
    #     items.insert(0, item.value)
    # items.insert(0, circle[0].value)
    #
    # print("Backward", items)
    # print()


def rotate(circle, index, number):
    steps = number % (len(circle) - 1)
    if steps == 0:
        return

    item = circle[index]

    # disconnect item from chain
    item.previous.next = item.next
    item.next.previous = item.previous

    position = item

    # travel to new location
    for i in range(steps):
        position = position.next

    # insert item in new location
    item.previous = position
    item.next = position.next
    position.next.previous = item
    position.next = item

    if debug:
        print_array(circle)


def nth_after_zero(circle, zero, n):
    item = zero
    for i in range(n % len(circle)):
        item = item.next

    return item.value


def mix(circle, numbers):
    for index, number in enumerate(numbers):
        if debug:
            print(number)
        rotate(circle, index, number)

def grove_coordinates(circle, zero):
    return sum(nth_after_zero(circle, zero, n) for n in [1000, 2000, 3000])

# Part 1
zero, circle = create_circle(numbers)
if debug:
    print_array(circle)
mix(circle, numbers)
solution(grove_coordinates(circle, zero))

# Part 2
decryption_key = 811589153
new_numbers = [number*decryption_key for number in numbers]
zero, circle = create_circle(new_numbers)
for i in range(10):
    mix(circle, new_numbers)
solution(grove_coordinates(circle, zero))
