import numpy.linalg

from aoc import solution
import parse
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

pattern = parse.compile('{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}')

positions = []
velocities = []

with open(filename) as f:
    for line in f:
        px, py, pz, vx, vy, vz = pattern.parse(line.strip())
        positions.append([px, py, pz])
        velocities.append([vx, vy, vz])

positions = np.array(positions, dtype=float)
velocities = np.array(velocities, dtype=float)

# Part 1
def intersect_path(p1, v1, p2, v2):
    """Find an intersection between the paths traced by two points"""

    m1 = v1[1] / v1[0]
    m2 = v2[1] / v2[0]

    A = np.array([[-m1, 1], [-m2, 1]])
    b = np.array([p1[1] - m1 * p1[0], p2[1] - m2 * p2[0]])

    try:
        pi = np.linalg.solve(A, b)
    except numpy.linalg.LinAlgError:
        return None

    # time of intersection
    t1 = (pi - p1) / v1
    t2 = (pi - p2) / v2

    if t1[0] < 0 or t2[0] < 0:
        return None

    return pi


if debug:
    lower, upper = 7, 27
else:
    lower, upper = 200000000000000, 400000000000000


c = 0
for i, (p1, v1) in enumerate(zip(positions[:, :2], velocities[:, :2])):
    for j, (p2, v2) in enumerate(zip(positions[:, :2], velocities[:, :2])):
        if i >= j:
            continue

        pi = intersect_path(p1, v1, p2, v2)
        if pi is not None and np.all((lower <= pi) & (pi <= upper)):
            c += 1


solution(c)

# Part 2
import sympy

# We're trying to solve for 3 coordinates and 3 velocities, and n_points times
# writing the intercept equation for one point gives 3 equation (one for each
# dimension)
# So 3 + 3 + npoints = 3 npoints,
# or npoints = 3

unknowns = prx, pry, prz, vrx, vry, vrz, t1, t2, t3 = sympy.symbols('prx pry prz vrx vry vrz t1 t2 t3')

pr = {'x': prx, 'y': pry, 'z': prz}
vr = {'x': vrx, 'y': vry, 'z': vrz}
t = {1: t1, 2: t2, 3: t3}

eqs = []
for i, (p, v) in enumerate(zip(positions[:3, :], velocities[:3, :]), 1):
    for d, pd, vd in zip('xyz', p, v):
        eqs.append(pd + vd * t[i] - pr[d] - vr[d] * t[i])

sol = sympy.solve(eqs, unknowns)

solution(sum(sol[0][:3]))