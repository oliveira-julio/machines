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


def lazy_eval(state: State, funcs):
    yield "init", state
    for func in funcs:
        state = func(state)
        yield func.__name__, state
    yield "end", state


if __name__ == "__main__":
    DEFAULT = State(array=[None, None, None], array_len=3)

    program = [move_right, move_right, move_right, move_left, move_left, move_left]
    old = DEFAULT
    for name, state in lazy_eval(DEFAULT, program):
        print("%10s %s" % (name, old))
        print("%10s %s" % ("'->", state))
        print()
        old = state
