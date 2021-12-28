from collections import Counter
from functools import cache
from itertools import product
import random

import networkx as nx
from rich.progress import track

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

LETTERS = 'ABCD'

MOVE_ENERGY = dict(zip(LETTERS, [1, 10, 100, 1000]))


class Cache:
    def __init__(self, roomsize):
        self.roomsize = roomsize
        self.solve_cache = {}
        self.graph = nx.Graph()
        self.build_graph()

    def build_graph(self):
        for i in range(10):
            self.graph.add_edge(i, i + 1)

        for room, roomtop in enumerate((2, 4, 6, 8)):
            roomstart = 11 + room * self.roomsize
            self.graph.add_edge(roomtop, roomstart)
            for roomi in range(self.roomsize - 1):
                self.graph.add_edge(roomstart + roomi, roomstart + roomi + 1)
                
    @cache
    def path(self, a, b):
        return nx.shortest_path(self.graph, a, b)


def parse(filename):
    with open(filename) as f:
        next(f)
        rows = [[c for c in line if c in LETTERS] for line in f]
    rows = [row for row in rows if row]
    rooms = list(zip(*rows))

    return Board(rooms)


class Board:
    def __init__(self, rooms=None, hall=None):
        """

        :param rooms: list of lists, left to right, top to bottom
        :param hall:
        """
        if hall is None:
            hall = ['.']*11

        if rooms is None:
            rooms = [['.', '.']]*4

        self.roomsize = len(rooms[0])

        self.spaces = hall[:]
        for room in rooms:
            self.spaces += room

    def copy(self):
        return Board(self.rooms(), self.hall())

    def rooms(self):
        n = self.roomsize
        return [self.spaces[11 + i * n:11 + i * n + n] for i in range(4)]

    def hall(self):
        return self.spaces[:11]

    def show(self):
        print("#"*13)
        hallstr = ''.join(['#', *self.hall(), '#'])
        r = self.rooms()
        print(hallstr)
        print(f"###{r[0][0]}#{r[1][0]}#{r[2][0]}#{r[3][0]}###")
        for i in range(1, self.roomsize):
            print(f"  #{r[0][i]}#{r[1][i]}#{r[2][i]}#{r[3][i]}#")
        print('  #########')

    def valid_move(self, move):
        a, b = move
        s = self.spaces

        pod = s[a]
        if pod == '.':
            # not moving an amphipod
            return False

        destination_room = LETTERS.index(pod)

        pp = self.path(a, b)
        if any(s[p] != '.' for p in pp[1:]):
            # Another token is in the way
            return False

        if b >= 11:  # to room
            # Amphipods will never move from the hallway into a room unless
            # that room is their destination room and that room contains no
            # amphipods which do not also have that room as their own destination.
            target_room, target_position = divmod((b - 11), self.roomsize)
            if target_room != destination_room:
                return False

            r = self.rooms()
            room = r[target_room]
            if any(contents not in ('.', pod) for contents in room):
                return False

            occupancy = room.count(pod) + 1
            correct_position = self.roomsize - occupancy
            if target_position != correct_position:
                return False
        else:  # to hallway
            if b in (2, 4, 6, 8):  # Can't stop at head of room
                return False

        if a >= 11:  # from room
            # Don't move away from the right location
            location_room, location_position = divmod(a - 11, self.roomsize)
            if location_room == destination_room:
                room = self.rooms()[location_room]
                occupancy = room.count(pod)
                correct_position = self.roomsize - occupancy
                if location_position == correct_position:
                    return False

        return True

    def valid_moves(self):
        moves = []

        # room to room
        for roomi, roomj in product(range(11, 11 + 4*self.roomsize), repeat=2):
            if roomi != roomj:
                move = (roomi, roomj)
                if self.valid_move(move):
                    moves.append(move)

        if moves:
            return moves[:1]

        # room to hallway, hallway to room
        for roomi in range(11, 11 + 4*self.roomsize):
            for halli in range(11):
                for move in ((roomi, halli), (halli, roomi)):
                    if self.valid_move(move):
                        moves.append(move)

        # Heuristics - if stuff in the halway can go home, do it
        home_moves = [(a, b) for (a, b) in moves if b >= 11]

        if home_moves:
            return home_moves[:1]

        return moves

    def move_energy(self, move):
        a, b = move
        pod = self.spaces[a]
        route = self.path(a, b)
        energy = MOVE_ENERGY[pod]*(len(route) - 1)
        return energy

    def move_order(self, move):
        a, b = move

        if b >= 11:
            return 0

        else:
            return len(self.path(a, b))

    def apply_move(self, move):
        a, b = move
        energy = self.move_energy(move)
        pod = self.spaces[a]
        self.spaces[b] = pod
        self.spaces[a] = '.'
        return energy

    def board_with_move(self, move):
        newboard = self.copy()
        energy = newboard.apply_move(move)
        return newboard, energy

    def solved(self):
        for target, room in zip(LETTERS, self.rooms()):
            if any(occupant != target for occupant in room):
                return False
        return True

    def solve(self, level=0):
        if self.solved():
            CACHE.solve_cache[self] = True, 0, []

        if self in CACHE.solve_cache:
            return CACHE.solve_cache[self]

        least_energy = None
        best_moves = []

        moves = self.valid_moves()

        if level == 0:
            tracker = track
        else:
            tracker = lambda x: x

        for move in tracker(moves):
            newboard, move_energy = self.board_with_move(move)
            if level <= 2:
                print(' '*level, move)
                newboard.show()

            solved, sub_energy, sub_moves = newboard.solve(level+1)
            CACHE.solve_cache[newboard] = solved, sub_energy, sub_moves

            if solved:
                total_energy = move_energy + sub_energy
                if level == 0:
                    print(f'Solved with {total_energy=} {level=} {len(CACHE.solve_cache)=}')
                if least_energy is None or total_energy < least_energy:
                    least_energy = total_energy
                    best_moves = [move, *sub_moves]
                # Greedy
                # return True, total_energy, best_moves


        CACHE.solve_cache[self] = least_energy is not None, least_energy, best_moves
        return least_energy is not None, least_energy, best_moves

    def apply_moves(self, moves, show=False):
        board = self
        energy = 0
        for i, move in enumerate(moves, 1):
            assert board.valid_move(move)
            # assert move in board.valid_moves()
            board, move_energy = board.board_with_move(move)
            energy += move_energy
            if show:
                print(f'Move {i}')
                board.show()

        return board, energy
    
    def path(self, a, b):
        return CACHE.path(a, b)

    def __hash__(self):
        return hash(tuple(self.spaces))

def random_search(starting_board):
    least_energy = None
    for i in track(range(10000)):
        board = starting_board.copy()
        energy = 0

        while moves := board.valid_moves():
            move = random.choice(moves)
            energy += board.move_energy(move)
            board.apply_move(move)

        if board.solved() and (not least_energy or energy < least_energy):
            least_energy = energy
            print(energy)

    return least_energy


if __name__ == "__main__":
    # Turns out random search is really effective in this problem
    board1 = parse('input.txt')
    CACHE = Cache(board1.roomsize)
    #
    # solution(random_search(board1))
    #
    # board2 = parse('input2.txt')
    # CACHE = Cache(board2.roomsize)
    # solution(random_search(board2))


    solved, energy, moves = board1.solve()
    assert solved

    solution(energy)

    solved, energy, moves = board2.solve()
    assert solved

    solution(energy)
