from octtree import range_overlap, Cube

def test_range_overlaps():
    assert range_overlap(0, 1, 3, 6) == None
    assert range_overlap(2, 4, 3, 6) == (3, 4)
    assert range_overlap(4, 5, 3, 6) == (4, 5)
    assert range_overlap(5, 7, 3, 6) == (5, 6)
    assert range_overlap(8, 9, 3, 6) == None


def test_cube1():
    world = Cube(0, 10, 0, 10, 0, 10, value=0, children=[])
    world.add(Cube(0, 5, 0, 5, 0, 5, value=1, children=[]))

    assert world.valuesum() == 125


def test_cube2():
    world = Cube(0, 10, 0, 10, 0, 10, value=0, children=[])
    other = Cube(0+2, 5+2, 0+2, 5+2, 0+2, 5+2, value=1, children=[])
    world.add(other)

    assert world.valuesum() == other.valuesum()

def test_cube3():
    world = Cube(-1000, 1000, -1000, 1000, -1000, 1000, value=0, children=[])
    other = Cube(23, 200, -500, 200, 0, 500, value=1, children=[])
    world.add(other)

    assert world.valuesum() == other.valuesum()
