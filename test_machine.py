from machine import State


def test_move_left():
    from machine import move_left

    base: State
    result: State

    base = move_left(State(acc=None, index=0, array=[None], array_len=1))
    result = State(acc=None, index=0, array=[None], array_len=1)
    assert base == result, "Move left trivial Case"

    base = move_left(State(acc=None, index=1, array=[None, None, None], array_len=3))
    result = State(acc=None, index=0, array=[None, None, None], array_len=3)
    assert base == result, "Moving to left"


def test_move_right():
    from machine import move_right

    base: State
    result: State

    base = move_right(State(acc=None, index=0, array=[None], array_len=1))
    result = State(acc=None, index=0, array=[None], array_len=1)
    assert base == result, "Move right trivial Case"

    base = move_right(State(acc=None, index=1, array=[None, None, None], array_len=3))
    result = State(acc=None, index=2, array=[None, None, None], array_len=3)
    assert base == result, "Moving to right"


def test_copy_cell():
    from machine import copy_cell

    base: State
    result: State

    base = copy_cell(State(acc=None, index=0, array=[1], array_len=1))
    result = State(acc=1, index=0, array=[1], array_len=1)
    assert base == result, "Copy trivial case"

    base = copy_cell(State(acc=1, index=0, array=[None], array_len=1))
    result = State(acc=None, index=0, array=[None], array_len=1)
    assert base == result, "Copy a blank cell -> blank acc"

    base = copy_cell(State(acc="a", index=1, array=["a", "b", "c"], array_len=3))
    result = State(acc="b", index=1, array=["a", "b", "c"], array_len=3)
    assert base == result, "Copying cell value to acc"


def test_erase_cell():
    from machine import erase_cell

    base: State
    result: State

    base = erase_cell(State(acc=None, index=0, array=[1], array_len=1))
    result = State(acc=None, index=0, array=[None], array_len=1)
    assert base == result, "Erase trivial case"

    base = erase_cell(State(acc=None, index=0, array=[None], array_len=1))
    result = State(acc=None, index=0, array=[None], array_len=1)
    assert base == result, "Erase a blank cell -> blank cell"

    base = erase_cell(State(acc=None, index=1, array=["a", "b", "c"], array_len=3))
    result = State(acc=None, index=1, array=["a", None, "c"], array_len=3)
    assert base == result, "Erasing cell value"


def test_set_cell():
    from machine import set_cell

    base: State
    result: State

    base = set_cell(State(acc=None, index=0, array=[1], array_len=1))
    result = State(acc=None, index=0, array=[None], array_len=1)
    assert base == result, "Set trivial case"

    base = set_cell(State(acc=1, index=0, array=[None], array_len=1))
    result = State(acc=1, index=0, array=[1], array_len=1)
    assert base == result, "Set a blank cell -> acc value"

    base = set_cell(State(acc="b", index=1, array=["a", None, "c"], array_len=3))
    result = State(acc="b", index=1, array=["a", "b", "c"], array_len=3)
    assert base == result, "Setting a cell"
