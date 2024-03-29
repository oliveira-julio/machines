from typing import NamedTuple
from typing import Any, List


class State(NamedTuple):
    acc: Any = None
    index: int = 0
    array: List[Any] = [None]
    array_len: int = 1
    pc: int = 0

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


def conditional(state: State) -> State:
    """
        Check if acc is equal the index cell.
        if is, increment pc + 1
        else, increment pc + 2

        Examples:
        conditional(State(acc=None, index=0, array=[1], array_len=1, pc=0))
        == State(acc=None, index=0, array=[1], array_len=1, pc=2)

        conditional(State(acc=1, index=0, array=[1], array_len=1), pc=0)
        == State(acc=1, index=0, array=[1], array_len=1, pc=1)
    """
    return state._replace(pc=state.pc + 1 + int(state.array[state.index] != state.acc))


def goto(fixed_pc: int):
    """
        Move state.pc to fixed_pc

        Examples:
        goto(0)(State(acc=1, index=0, array=[1], array_len=1), pc=0)
        == State(acc=1, index=0, array=[1], array_len=1, pc=0)

        goto(10)(State(acc=None, index=0, array=[1], array_len=1, pc=0))
        == State(acc=None, index=0, array=[1], array_len=1, pc=10)
    """

    def _goto(state: State) -> State:
        return state._replace(pc=fixed_pc)

    return _goto


def iadd(state: State) -> State:
    """
        Move state.pc to fixed_pc

        Examples:
        iadd(State(acc=None, index=0, array=[1], array_len=1), pc=0)
        == State(acc=1, index=0, array=[1], array_len=1, pc=0)

        iadd(State(acc=10, index=1, array=[1, 2, 3], array_len=1, pc=0))
        == State(acc=12, index=1, array=[1, 2, 3], array_len=1, pc=0)
    """
    cell = state.array[state.index] or 0
    return state._replace(acc=state.acc + cell)


def identity(state: State) -> State:
    """
        return the given state

        Examples:
        identity(State(acc=None, index=0, array=[1], array_len=1), pc=0)
        == State(acc=None, index=0, array=[1], array_len=1, pc=0)

        identity(State(acc=10, index=1, array=[1, 2, 3], array_len=1, pc=0))
        == State(acc=10, index=1, array=[1, 2, 3], array_len=1, pc=0)
    """
    return state


def lazy_eval(state: State, funcs):
    yield "init", state
    pc = state.pc
    end = len(funcs)
    while pc < end:
        func = funcs[pc]
        state = func(state)

        if state.pc == pc:
            pc = state.pc + 1
            state = state._replace(pc=pc)
        else:
            pc = state.pc
        yield func.__name__, state
    yield "end", state


if __name__ == "__main__":

    def run(state: State, program):
        old = state
        for name, state in lazy_eval(state, program):
            print("%10s %s" % (name, old))
            print("%10s %s" % ("'->", state))
            print()
            old = state

    # inverse abc -> cba
    inverse_commands = [
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
    inverse_state = State(array=["a", "b", "c", None], array_len=4)
    inverse_program = (inverse_state, inverse_commands)

    # summation 10, 0, -1, 0 -> 0, 0, -1, 55
    summation_commands = [
        copy_cell,  # 0
        move_right,  # 1
        conditional,
        goto(15),
        move_right,
        move_right,
        iadd,
        set_cell,
        move_left,
        copy_cell,
        move_left,
        move_left,
        iadd,
        set_cell,
        goto(1),
        identity,  # 15
    ]
    summation_state = State(array=[10, 0, -1, 0], array_len=4)
    summation_program = (summation_state, summation_commands)

    run(*summation_program)
    run(*inverse_program)
