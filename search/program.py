# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers

from .core import CellState, Coord, Direction, MoveAction
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
    
    # Find the starting position of the red frog
    red_start = None
    for coord, cell_state in board.items():
        if cell_state == CellState.RED:
            red_start = coord
            break
    
    # Return None if no red frog is found
    if not red_start:
        return None

    # Define valid moves as down, down-left, down-right
    valid_moves = [Direction.Down, Direction.DownLeft, Direction.DownRight]

    # Initialise a queue and visited set for BFS
    queue = deque()
    visited = set()

    # Add the starting position to the queue
    queue.append((red_start, []))
    visited.add(red_start)

    # Find the shortest path to the last row using BFS
    while queue:
        current_position, path = queue.popleft()

        # Check if the current position is in the last row
        if current_position.y == 0:
            return path

        # Generate all possible next positions
        for move in valid_moves:
            next_position = current_position + move

            # check if the next position is valid. This means there is a lily pad adjacent or a frog followed immediately by a lily pad.  The position is not visited. 
            adjacent_move = board[next_position] == CellState.LILY_PAD
            hop = next_position + move in board and board[next_position + move] == CellState.LILY_PAD
            if next_position in board and (adjacent_move or hop) and next_position not in visited:
                queue.append((next_position, path + [MoveAction(next_position, [move])]))
                visited.add(next_position)

    # If no path is found, return None
    return None