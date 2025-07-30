import random
import time

# from https://www.labri.fr/perso/nrougier/from-python-to-numpy/#code-vectorization


def compute_neighbours(current_state_zero_bordered: list[list[int]]) -> list[list[int]]:
    """
    Compute the number of neighbours for each cell in the Game of Life grid.

    Args:
        Z (list[list[int]]): The current state of the Game of Life. (with a border of zeros)
    Returns:
        list[list[int]]: A grid of the same size as Z, where each cell contains
                          the number of live neighbours for the corresponding cell in Z.
    """
    shape = len(current_state_zero_bordered), len(current_state_zero_bordered[0])
    neighbors_count_arr = [
        [
            0,
        ]
        * (shape[0])
        for i in range(shape[1])
    ]
    for x in range(1, shape[0] - 1):
        for y in range(1, shape[1] - 1):
            neighbors_count_arr[x][y] = (
                current_state_zero_bordered[x - 1][y - 1]
                + current_state_zero_bordered[x][y - 1]
                + current_state_zero_bordered[x + 1][y - 1]
                + current_state_zero_bordered[x - 1][y]
                + current_state_zero_bordered[x + 1][y]
                + current_state_zero_bordered[x - 1][y + 1]
                + current_state_zero_bordered[x][y + 1]
                + current_state_zero_bordered[x + 1][y + 1]
            )
    return neighbors_count_arr


def state_iterate(Z):
    """
    Iterate the state of the Game of Life.

    Args:
        Z (list[list[int]]): The current state of the Game of Life. (with a border of zeros)
    """
    shape = len(Z), len(Z[0])
    N = compute_neighbours(Z)
    for x in range(1, shape[0] - 1):
        for y in range(1, shape[1] - 1):
            if Z[x][y] == 1 and (N[x][y] < 2 or N[x][y] > 3):
                Z[x][y] = 0
            elif Z[x][y] == 0 and N[x][y] == 3:
                Z[x][y] = 1
    return Z


def state_print_current(Z):
    # Remove the first and last row, and first and last column from each row
    trimmed_Z = [row[1:-1] for row in Z[1:-1]]
    for row in trimmed_Z:
        # Display 1 as 'X' and 0 as '.'
        print("".join("X" if cell == 1 else "." for cell in row))
        # display 1 in red and 0 in green
        # print("".join(str(cell) for cell in row))


def state_add_zero_border(Z):
    state_width = len(Z[0])
    # Add a border of zeros around the initial state
    return (
        [[0] * (state_width + 2)]
        + [[0] + row + [0] for row in Z]
        + [[0] * (state_width + 2)]
    )


def state_run_generation(
    state_initial, state_generation_count=10, delay_inter_generation_seconds=0.1
):
    """
    Run the Game of Life for a given number of generations.

    Args:
        state_initial (list[list[int]]): The initial state of the Game of Life.
        state_generation_count (int): The number of generations to run.
    """

    # Add a border of zeros around the initial state to ease the neighbour counting
    state_zero_bordered = state_add_zero_border(state_initial)

    print(f"initial state:")
    state_print_current(state_zero_bordered)
    # wait 1 second before the next iteration
    time.sleep(delay_inter_generation_seconds)

    for iteration_count in range(state_generation_count):
        # clear the console
        print("\033c", end="")

        state_zero_bordered = state_iterate(state_zero_bordered)
        print(f"After {iteration_count+1} iterations:")
        state_print_current(state_zero_bordered)

        # wait 1 second before the next iteration
        time.sleep(delay_inter_generation_seconds)


##### Example usage


def initial_state_random(state_width=10, state_height=10, random_seed=None):
    initial_living_cell_count = (state_width * state_height) // 2

    # setup an empty initial state
    state_initial = [[0 for _ in range(state_width)] for _ in range(state_height)]

    # specify the seed for reproducibility
    if( random_seed is not None):
        random.seed(random_seed)

    # add initial live cells at random positions
    for _ in range(initial_living_cell_count):
        x = random.randint(0, state_width - 1)
        y = random.randint(0, state_height - 1)
        state_initial[y][x] = 1

    # setup a random initial state
    # state_initial = [[random.randint(0, 1) for _ in range(state_width)] for _ in range(state_height)]

    return state_initial


def initial_state_original():
    """
    Original initial state from the Game of Life example.

    from https://www.labri.fr/perso/nrougier/from-python-to-numpy/#code-vectorization
    """
    initial_state = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]]
    return initial_state


#################################################################

# state_initial = initial_state_random()
state_initial = initial_state_original()

state_run_generation(
    state_initial=state_initial,
    state_generation_count=4,
    delay_inter_generation_seconds=2,
)
