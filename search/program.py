# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers
# Alisa Blakeney, 1178580
# Using A* algorithm to find the shortest path for the red frog


from .core import BOARD_N, CellState, Coord, Direction, MoveAction
from .utils import render_board
from collections import deque

def search(
    board: dict[Coord, CellState]
) -> list[MoveAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `CellState` instances which can be one of
            `CellState.RED`, `CellState.BLUE`, or `CellState.LILY_PAD`.
    
    Returns:
        A list of "move actions" as MoveAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...``
    # ... (your solution goes here!)
    # ...

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    # return [
    #     MoveAction(Coord(0, 5), [Direction.Down]),
    #     MoveAction(Coord(1, 5), [Direction.DownLeft]),
    #     MoveAction(Coord(3, 3), [Direction.Left]),
    #     MoveAction(Coord(3, 2), [Direction.Down, Direction.Right]),
    #     MoveAction(Coord(5, 4), [Direction.Down]),
    #     MoveAction(Coord(6, 4), [Direction.Down]),
    # ]
    
    def is_goal(state: dict[Coord, CellState]) -> bool:
        # Check if any red frog is in the last row (BOARD_N - 1)
        for coord, cell in state.items():
            if cell == CellState.RED and coord.r == BOARD_N - 1:
                return True
        return False

    def get_successors(state: dict[Coord, CellState], path: list[MoveAction]) -> list[tuple[dict[Coord, CellState], list[MoveAction]]]:
        successors = []
        valid_directions = [Direction.Down, Direction.DownLeft, Direction.DownRight, Direction.Left, Direction.Right]
        for coord, cell in state.items():
            if cell == CellState.RED:
                # Check for single adjacent moves to a lily pad
                for direction in valid_directions:
                    try:
                        new_coord = coord + direction
                        if 0 <= new_coord.r < BOARD_N and 0 <= new_coord.c < BOARD_N:
                            if abs(new_coord.r - coord.r) <= 1 and abs(new_coord.c - coord.c) <= 1:
                                if state.get(new_coord) == CellState.LILY_PAD:
                                    new_state = state.copy()
                                    new_state[new_coord] = CellState.RED
                                    del new_state[coord]  
                                    successors.append((new_state, path + [MoveAction(coord, direction)]))
                    except ValueError:
                        continue

                # Check for jumps over frogs onto a lily pad
                def find_jumps(start_coord, current_coord, visited, current_directions):
                    for direction in valid_directions:
                        try:
                            intermediate_coord = current_coord + direction
                            jump_coord = intermediate_coord + direction
                            if (
                                0 <= jump_coord.r < BOARD_N
                                and 0 <= jump_coord.c < BOARD_N
                                and state.get(intermediate_coord) in {CellState.RED, CellState.BLUE}
                                and state.get(jump_coord) == CellState.LILY_PAD
                                and jump_coord not in visited
                            ):
                                new_directions = current_directions + [direction]
                                new_state = state.copy()
                                new_state[jump_coord] = CellState.RED
                                del new_state[start_coord]
                                new_state[intermediate_coord] = CellState.LILY_PAD
                                visited.add(jump_coord)

                                # Recursive continuation
                                find_jumps(start_coord, jump_coord, visited, new_directions)

                                # After finishing the sequence, add the move
                                successors.append(
                                    (new_state, path + [MoveAction(start_coord, new_directions)])
                                )
                        except ValueError:
                            continue

                find_jumps(coord, coord, {coord}, [])

        return successors

    start_state = board
    queue = deque([(start_state, [])]) # Use deque for BFS
    visited = set() # Use a set to track visited states
    visited.add(frozenset(start_state.items())) # Use frozenset to make it hashable

    while queue:
        current_state, path = queue.popleft() 

        if is_goal(current_state):
            return path

        for successor, new_path in get_successors(current_state, path): 
            successor_key = frozenset(successor.items())  
            if successor_key not in visited:
                visited.add(successor_key)
                queue.append((successor, new_path))

    return None