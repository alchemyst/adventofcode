from solve import get_instructions, process


def test1():
    # For example, here is an ALU program which takes an input number, negates it,
    # and stores it in x:

    instructions = get_instructions(
        """
        inp x
        mul x -1
    """
    )

    result = process(instructions, [2])

    assert result["x"] == -2


def test2():
    # Here is an ALU program which takes two input numbers, then sets z to 1 if
    # the second input number is three times larger than the first input number,
    # or sets z to 0 otherwise:
    instructions = get_instructions(
        """
        inp z
        inp x
        mul z 3
        eql z x
    """
    )

    result = process(instructions, [2, 6])
    assert result["z"] == 1

    result = process(instructions, [2, 2])
    assert result["z"] == 0


def test3():
    # Here is an ALU program which takes a non-negative integer as input, converts
    # it into binary, and stores the lowest (1's) bit in z, the second-lowest (2's)
    # bit in y, the third-lowest (4's) bit in x, and the fourth-lowest (8's) bit in w:

    instructions = get_instructions(
        """
        inp w
        add z w
        mod z 2
        div w 2
        add y w
        mod y 2
        div w 2
        add x w
        mod x 2
        div w 2
        mod w 2
    """
    )

    binvalue = "1010"
    result = process(instructions, [int(binvalue, 2)])

    assert result["w"] == 1
    assert result["x"] == 0
    assert result["y"] == 1
    assert result["z"] == 0
