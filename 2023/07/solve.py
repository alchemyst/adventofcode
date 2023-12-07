from aoc import solution
from collections import Counter
from functools import cache, partial
import parse

debug = False
filename = 'test.txt' if debug else 'input.txt'

# 6 Five of a kind, where all five cards have the same label: AAAAA
# 5 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# 4 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# 3 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# 2 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# 1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# 0 High card, where all cards' labels are distinct: 23456
HAND_VALUES = ((1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 2, 2), (1, 1, 3), (2, 3), (1, 4), (5,))


def sort_hand(hand):
    return ''.join(sorted(hand))


@cache
def kind(cards, joker, hand):
    counts = Counter(hand).values()

    if counts == (5,):
        return 6  # Five of a kind even if jokers

    return (
        max(
            kind(cards, joker, sort_hand(hand.replace('J', card)))
            for card in cards
            if card != 'J'
        )
        if joker and 'J' in hand
        else HAND_VALUES.index(tuple(sorted(counts)))
    )


@cache
def card_strengths(cards, hand):
    return tuple(cards.index(card) for card in hand)


@cache
def keyfunc(cards, joker, hand_bid):
    hand, _ = hand_bid
    return kind(cards, joker, sort_hand(hand)), card_strengths(cards, hand)


def solve(cards, joker):
    local_keyfunc = partial(keyfunc, cards, joker)
    return sum(
        rank * bid
        for rank, (hand, bid) in enumerate(sorted(hands, key=local_keyfunc), 1)
    )


parser = parse.compile('{} {:d}')
hands = [parser.parse(line.strip()) for line in open(filename)]


# Part 1
solution(solve('AKQJT98765432'[::-1], False))

# Part 2
solution(solve('AKQT98765432J'[::-1], True))
