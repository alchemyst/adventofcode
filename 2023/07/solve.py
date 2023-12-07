from aoc import solution
from collections import Counter
from functools import cache


debug = False
filename = 'test.txt' if debug else 'input.txt'


def sort_hand(hand):
    return ''.join(sorted(hand))

class Evaluator:
    def __init__(self, cards):
        self.cards = cards

    @cache
    def kind(self, hand):
        # 6 Five of a kind, where all five cards have the same label: AAAAA
        # 5 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        # 4 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        # 3 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        # 2 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        # 1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        # 0 High card, where all cards' labels are distinct: 23456
        counter = Counter(hand)
        values = counter.values()
        if 5 in values:
            return 6  # Five of a kind
        elif 4 in values:
            return 5  # Four of a kind
        elif 3 in values:
            if 2 in values:
                return 4  # Full house'
            else:
                return 3  # Three of a kind'
        elif 2 in values:
            if len(counter) == 3:
                return 2 # Two pair
            else:
                return 1 # One pair'
        else:
            return 0 # High card

    @cache
    def card_strengths(self, hand):
        return tuple(self.cards.index(card) for card in hand)


    @cache
    def keyfunc(self, hand_bid):
        hand, _ = hand_bid
        return self.kind(sort_hand(hand)), self.card_strengths(hand)


class JokerEvaluator(Evaluator):
    @cache
    def kind(self, hand):
        # 6 Five of a kind, where all five cards have the same label: AAAAA
        # 5 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        # 4 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        # 3 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        # 2 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        # 1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        # 0 High card, where all cards' labels are distinct: 23456
        counter = Counter(hand)
        values = counter.values()
        if 5 in values:
            return 6  # Five of a kind even if jokers

        if 'J' in hand:
            return max(self.kind(sort_hand(hand.replace('J', card))) for card in self.cards if card != 'J')
        if 4 in values:
            return 5  # Four of a kind
        elif 3 in values:
            if 2 in values:
                return 4  # Full house'
            else:
                return 3  # Three of a kind'
        elif 2 in values:
            if len(counter) == 3:
                return 2 # Two pair
            else:
                return 1 # One pair'
        else:
            return 0 # High card



part1_evaluator = Evaluator('AKQJT98765432'[::-1])

hands = []
with open(filename) as f:
    for line in f:
        line = line.strip()
        hand, bid = line.split(' ')
        hands.append((hand, int(bid)))

def solve(evaluator):
    s = 0
    for rank, (hand, bid) in enumerate(sorted(hands, key=evaluator.keyfunc), 1):
        s += rank * bid
    return s


# Part 1
solution(solve(part1_evaluator))

# Part 2
part2_evaluator = JokerEvaluator('AKQT98765432J'[::-1])

solution(solve(part2_evaluator))