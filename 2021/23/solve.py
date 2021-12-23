from functools import cache
from itertools import product

import networkx as nx
from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

LETTERS = 'ABCD'

MOVE_ENERGY = dict(zip(LETTERS, [1, 10, 100, 1000]))

SOLVE_CACHE = {}

def parse(filename):
    with open(filename) as f:
        next(f)
        rows = [[c for c in line if c in LETTERS] for line in f]
    rows = [row for row in rows if row]
    rooms = list(zip(*rows))

    return Board(rooms)

GRAPH = nx.Graph()
GRAPH.add_edges_from([
    (0, 1),
    (1, 2),

    (2, 11),
    (11, 12),
    (2, 3),

    (3, 4),

    (4, 13),
    (13, 14),
    (4, 5),

    (5, 6),

    (6, 15),
    (15, 16),
    (6, 7),

    (7, 8),

    (8, 17),
    (17, 18),

    (8, 9),
    (9, 10),
])



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

        # build graph
        self.graph = nx.Graph()

        for i in range(10):
            self.graph.add_edge(i, i+1)

        for room, roomtop in enumerate((2, 4, 6, 8)):
            roomstart = 11 + room*self.roomsize
            self.graph.add_edge(roomtop, roomstart)
            for roomi in range(self.roomsize-1):
                self.graph.add_edge(roomstart + roomi, roomstart + roomi + 1)

    @cache
    def path(self, a, b):
        return nx.shortest_path(self.graph, a, b)

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

        if a < 11 and b >= 11:  # hallway to room
            # Amphipods will never move from the hallway into a room unless
            # that room is their destination room and that room contains no
            # amphipods which do not also have that room as their own destination.
            target_room = int((b - 11)//self.roomsize)
            if target_room != destination_room:
                return False

            r = self.rooms()
            if any(contents not in ('.', pod) for contents in r[target_room]):
                return False
        else:  # room to hallway
            if b in (2, 4, 6, 8):  # Can't stop at head of room
                return False

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

        # room to room - didn't get this working right
        # for roomi, roomj in product(range(11, 11 + 4*self.roomsize), repeat=2):
        #     if roomi != roomj:
        #         moves.append((roomi, roomj))

        # room to hallway, hallway to room
        for roomi in range(11, 11 + 4*self.roomsize):
            for halli in range(11):
                for move in ((roomi, halli), (halli, roomi)):
                    if self.valid_move(move):
                        moves.append(move)

        return moves

    def move_energy(self, move):
        a, b = move
        pod = self.spaces[a]
        route = self.path(a, b)
        energy = MOVE_ENERGY[pod]*(len(route) - 1)
        return energy

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

    def solve(self, level=0, maxlevel=None, energy_budget=None):
        if self.solved():
            SOLVE_CACHE[self] = True, 0, []

        if self in SOLVE_CACHE:
            return SOLVE_CACHE[self]

        if maxlevel and level > maxlevel:
            return False, None, []

        least_energy = None
        best_moves = []
        for move in self.valid_moves():
            newboard, move_energy = self.board_with_move(move)
            if energy_budget and move_energy > energy_budget:
                return False, least_energy, best_moves

            if least_energy:
                sub_energy_budget = least_energy - move_energy
            elif energy_budget:
                sub_energy_budget = energy_budget - move_energy
            else:
                sub_energy_budget = None

            solved, sub_energy, sub_moves = newboard.solve(level+1, maxlevel, sub_energy_budget)

            if solved:
                SOLVE_CACHE[newboard] = solved, sub_energy, sub_moves
                total_energy = move_energy + sub_energy
                # print('Solved with', total_energy)
                if least_energy is None or total_energy < least_energy:
                    least_energy = total_energy
                    best_moves = [move, *sub_moves]

        return least_energy is not None, least_energy, best_moves

    def apply_moves(self, moves, show=False):
        board = self
        energy = 0
        for i, move in enumerate(moves, 1):
            assert board.valid_move(move)
            assert move in board.valid_moves()
            board, move_energy = board.board_with_move(move)
            energy += move_energy
            if show:
                print(f'Move {i}')
                board.show()

        return board, energy

    def __hash__(self):
        return hash(tuple(self.spaces))

if __name__ == "__main__":
    board1 = parse('input.txt')
    solved, energy, moves = board1.solve()
    assert solved

    solution(energy)

    SOLVE_CACHE.clear()
    board2 = parse('input2.txt')
    solved, energy, moves = board2.solve()
    assert solved

    solution(energy)
