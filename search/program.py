# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers
# Alisa Blakeney, 1178580
# Using A* algorithm to find the shortest path for the red frog


from .core import BOARD_N, CellState, Coord, Direction, MoveAction
from .utils import render_board
from collections import deque
import heapq


# Function to calculate the Manhattan distance heuristic for A* search
def manhattan_distance(coord: Coord) -> int:
# The Manhattan distance is the vertical distance to the last row (goal row)
    return BOARD_N - 1 - coord.r

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
    # Goal is achieved if the red frog is in the last row (BOARD_N - 1)
        for coord, cell in state.items():
            if cell == CellState.RED and coord.r == BOARD_N - 1:
                return True
        return False

    # Get all possible successor states from the current state
    def get_successors(state: dict[Coord, CellState], path: list[MoveAction]) -> list[tuple[dict[Coord, CellState], list[MoveAction]]]: # List of (state, path) tuples
        successors = []
        # Iterate through all coordinates and cells in the current state
        for coord, cell in state.items():
            if cell == CellState.RED:
                # Check for jumps over frogs onto a lily pad
                def find_jumps(current_coord, visited, current_path, directions):
                    # print("PATH", current_path)
                    consecutive_jumps = []
                    new_jump_coord = Coord(0, 0)
                    # found_jump = False
                    for direction in Direction:
                        try:
                            # Calculate intermediate and jump coordinates
                            intermediate_coord = current_coord + direction
                            jump_coord = intermediate_coord + direction
                            if (
                                0 <= jump_coord.r < BOARD_N # Check if the jump coordinate is within the board
                                and 0 <= jump_coord.c < BOARD_N # Check if the jump coordinate is within the board
                                and state.get(intermediate_coord) in {CellState.RED, CellState.BLUE} # Check if the intermediate coordinate has a frog
                                and state.get(jump_coord) == CellState.LILY_PAD # Check if the jump coordinate has a lily pad
                                and jump_coord not in visited
                            ):
                                # found_jump = True
                                if abs(jump_coord.r - coord.r) <= 2 and abs(jump_coord.c - coord.c) <= 2: # Check the jump will not wrap around the board
                                    # Create a new state with the jump applied
                                    new_state = state.copy() # Copy the current state
                                    new_state[jump_coord] = CellState.RED # Move the red frog to the jump coordinate
                                    del new_state[current_coord] #remove the lily pad from the current coordinate
                                    new_path = current_path + [MoveAction(current_coord, direction)]
                                    visited.add(jump_coord)
                                    find_jumps(jump_coord, visited, new_path, directions + [direction])
                                    # successors.append((new_state, path + [MoveAction(coord, directions)]))
                                    consecutive_jumps.append((new_state, path + [MoveAction(coord, directions + [direction])]))
                                    # print("JUMPS",consecutive_jumps)
                        except ValueError:
                            continue

                    # Append all found consecutive jumps as successors
                    successors.extend(consecutive_jumps)


                    # if not found_jump and len(current_path) > 0:
                        # print("JUMPS",consecutive_jumps)
                        # successors.append((new_state, path + [MoveAction(coord, directions)]))
                        # successors.extend(consecutive_jumps)

                # Start finding jumps from the current coordinate
                find_jumps(coord, {coord}, path, [])

                # Check for single adjacent moves to a lily pad
                for direction in Direction:
                    try:
                        # Calculate new coordinate after moving in the given direction
                        new_coord = coord + direction
                        if 0 <= new_coord.r < BOARD_N and 0 <= new_coord.c < BOARD_N:
                            if abs(new_coord.r - coord.r) <= 1 and abs(new_coord.c - coord.c) <= 1:
                                if state.get(new_coord) == CellState.LILY_PAD:
                                    # Create a new state with the move applied
                                    new_state = state.copy()
                                    new_state[new_coord] = CellState.RED 
                                    del new_state[coord]
                                    successors.append((new_state, path + [MoveAction(coord, direction)]))
                    except ValueError:
                        continue
        return successors
    
    # Initialize the start state and priority queue for A* search
    start_state = board
    open_list = []
    # Push the start state to the priority queue with initial cost 0
    heapq.heappush(open_list, (0, id(start_state), start_state, []))
    visited = set()  # Set to keep track of visited states
    visited.add(frozenset(start_state.items()))

    # A* search loop
    while open_list:
        # Pop the state with the lowest cost from the priority queue
        _, _, current_state, path = heapq.heappop(open_list)

        # Check if the goal state is reached
        if is_goal(current_state):
            return path

        # Get all successor states from the current state
        for successor, new_path in get_successors(current_state, path):
            successor_key = frozenset(successor.items()) # Convert the state to a hashable key
            if successor_key not in visited:
                visited.add(successor_key) 
                # Calculate the cost as the length of the path plus the heuristic
                cost = len(new_path) + manhattan_distance(next(iter(successor.keys()))) 
                # Push the successor state to the priority queue with the calculated cost
                heapq.heappush(open_list, (cost, id(successor), successor, new_path))

    return None  # Return None if no path is found