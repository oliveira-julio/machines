from typing import NamedTuple
from typing import Any, List


class State(NamedTuple):
    acc: Any = None
    index: int = 0
    array: List[Any] = [None]
    array_len: int = 1

    def bind(self, func):
        return func(self)


def move_left(state: State) -> State:
    """
    Move index one cell to left. If index in first cell, so return state

    Examples:
    move_left(State(acc=None, index=0, array=[None], array_len=1))
    == State(acc=None, index=0, array=[None], array_len=1)

    move_left(State(acc=None, index=1, array=[None, None, None], array_len=3))
    == State(acc=None, index=0, array=[None, None, None], array_len=3)
    """
    assert state.index >= 0
    if not state.index:
        return state

    assert state.index > 0
    return state._replace(index=state.index - 1)


def move_right(state: State) -> State:
    """
    Move index one cell to right. If index in the last cell, so return state

    Examples:
    move_right(State(acc=None, index=0, array=[None], array_len=1))
    == State(acc=None, index=0, array=[None], array_len=1)

    move_right(State(acc=None, index=1, array=[None, None, None], array_len=3))
    == State(acc=None, index=2, array=[None, None, None], array_len=3)
    """
    assert state.index < state.array_len
    if state.index == state.array_len - 1:
        return state

    assert state.index < state.array_len - 1
    return state._replace(index=state.index + 1)


def copy_cell(state: State) -> State:
    """
    Copy value of cell to acc. The old acc value is lost.

    Examples:
    copy_cell(State(acc=None, index=0, array=[1], array_len=1))
    == State(acc=1, index=0, array=[1], array_len=1)

    copy_cell(State(acc=1, index=0, array=[None], array_len=1))
    == State(acc=None, index=0, array=[None], array_len=1)

    copy_cell(State(acc='a', index=1, array=['a', 'b', 'c'], array_len=3))
    == State(acc='b', index=1, array=['a', 'b', 'c'], array_len=3)
    """
    assert state.index < state.array_len
    return state._replace(acc=state.array[state.index])


def erase_cell(state: State) -> State:
    """
    Erase value of cell. The cell value is lost.

    Examples:
    erase_cell(State(acc=None, index=0, array=[1], array_len=1))
    == State(acc=None, index=0, array=[None], array_len=1)

    erase_cell(State(acc=None, index=0, array=[None], array_len=1))
    == State(acc=None, index=0, array=[None], array_len=1)

    erase_cell(State(acc=None, index=1, array=['a', 'b', 'c'], array_len=3))
    == State(acc=None, index=1, array=['a', None, 'c'], array_len=3)
    """
    assert state.index < state.array_len
    return state._replace(
        array=state.array[: state.index] + [None] + state.array[state.index + 1 :]
    )


def set_cell(state: State) -> State:
    """
    Erase value of cell. The cell value is lost.

    Examples:
    set_cell(State(acc=None, index=0, array=[1], array_len=1))
    == State(acc=None, index=0, array=[None], array_len=1)

    set_cell(State(acc=1, index=0, array=[None], array_len=1))
    == State(acc=1, index=0, array=[1], array_len=1)

    set_cell(State(acc='b', index=1, array=['a', 'b', 'c'], array_len=3))
    == State(acc='b', index=1, array=['a', 'b', 'c'], array_len=3)
    """
    assert state.index < state.array_len
    return state._replace(
        array=state.array[: state.index] + [state.acc] + state.array[state.index + 1 :]
    )


def lazy_eval(state: State, funcs):
    yield "init", state
    for func in funcs:
        state = func(state)
        yield func.__name__, state
    yield "end", state


if __name__ == "__main__":
    DEFAULT = State(array=["a", "b", "c", None], array_len=4)

    # inverse abc -> cba
    program = [
        copy_cell,
        erase_cell,
        move_right,
        move_right,
        move_right,
        set_cell,
        move_left,
        copy_cell,
        erase_cell,
        move_left,
        move_left,
        set_cell,
        move_right,
        move_right,
        move_right,
        copy_cell,
        erase_cell,
        move_left,
        set_cell,
    ]
    old = DEFAULT
    for name, state in lazy_eval(DEFAULT, program):
        print("%10s %s" % (name, old))
        print("%10s %s" % ("'->", state))
        print()
        old = state
