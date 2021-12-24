import pytest

import solve
from solve import Board, Cache

solve.CACHE = Cache(2)

def test_solved():
    board = Board(
        [list(room) for room in ['AA', 'BB', 'CC', 'DD']],
        list('.' * 11),
    )

    assert board.solved()


def test_notsolved():
    board = Board(
        [list(room) for room in ['.A', 'BB', 'CC', 'DD']],
        list('A' + '.' * 10),
    )

    assert not board.solved()


def test_valid_moves():
    board = Board(
        [list(room) for room in ['AA', 'BB', '..', 'DD']],
        list('CC' + '.' * 9),
    )

    moves = (
        (1, 16),
        (0, 15),
    )

    final, energy = board.apply_moves(moves)

def test_invalid_moves():
    board = Board(
        [list(room) for room in ['AA', 'BB', '..', 'DD']],
        list('CC' + '.' * 9),
    )

    assert not board.valid_move((0, 16))


def test_sample_solution():
    board = Board(
        [list(room) for room in ['.B', '.A', 'CC', 'DD']],
        list('AB' + '.' * 9),
    )
    moves = (
        (12, 5),
        (14, 3),
        (3, 12),
        (5, 14),
        (1, 13),
        (0, 11)
    )

    final, energy = board.apply_moves(moves)
    assert final.solved()

def test_example():
    board = Board(
        [list(room) for room in ['BA', 'CD', 'BC', 'DA']]
    )

    moves = (
        (15, 3),
        (13, 5),
        (5, 15),
        (14, 5),
        (3, 14),
        (11, 3),
        (3, 13),
        (17, 7),
        (18, 9),
        (7, 18),
        (5, 17),
        (9, 11),
    )

    final, energy = board.apply_moves(moves)

    assert final.solved()
    assert energy == 12521

# def test_example_room_to_room():
#     board = Board(
#         [list(room) for room in ['BA', 'CD', 'BC', 'DA']]
#     )
#
#     moves = (
#         (15, 3),
#         (13, 5),
#         (5, 15),
#         (14, 5),
#         (3, 14),
#         (11, 13),
#         (17, 7),
#         (18, 9),
#         (7, 18),
#         (5, 17),
#         (9, 11),
#     )
#
#     final, energy = board.apply_moves(moves)
#
#     assert final.solved()
#     assert energy == 12521

def test_solver_simple1():
    board = Board(
        [list(room) for room in ['BA', 'AB', 'CC', 'DD']],
    )

    solved, energy, moves = board.solve()
    assert solved

def test_solver_simple2():
    board = Board(
        [list(room) for room in ['DA', 'BB', 'CC', 'AD']],
    )

    solved, energy, moves = board.solve()
    assert solved

def test_solver_simple3():
    board = Board(
        [list(room) for room in ['DD', 'BB', 'CC', 'AA']],
    )

    solved, energy, moves = board.solve(maxlevel=8)
    assert solved
