from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    directions = []

    if x >= 2:
        directions.append((-2, 0))

    if y + 2 < len(grid[0]):
        directions.append((0, 2))

    if not directions:
        return grid

    dx, dy = choice(directions)

    wall_x = x + dx // 2
    wall_y = y + dy // 2
    grid[wall_x][wall_y] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for x, y in empty_cells:
        direction = choice(["up", "right"])
        may_go_up = x > 1
        may_go_right = y < cols - 2

        if direction == "up":
            if may_go_up:
                grid[x - 1][y] = " "
            elif may_go_right:
                grid[x][y + 1] = " "
        elif direction == "right":
            if may_go_right:
                grid[x][y + 1] = " "
            elif may_go_up:
                grid[x - 1][y] = " "

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    cells_to_update = set()

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                neighbors = []
                if x > 0:
                    neighbors.append((x - 1, y))
                if x < rows - 1:
                    neighbors.append((x + 1, y))
                if y > 0:
                    neighbors.append((x, y - 1))
                if y < cols - 1:
                    neighbors.append((x, y + 1))

                for nx, ny in neighbors:
                    if grid[nx][ny] == 0 or grid[nx][ny] == " ":
                        cells_to_update.add((nx, ny))

    for nx, ny in cells_to_update:
        grid[nx][ny] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    path = []
    current = exit_coord
    rows, cols = len(grid), len(grid[0])

    current_k = grid[current[0]][current[1]]

    if not isinstance(current_k, int) or current_k == 0:
        return None

    path.append(current)

    while current_k > 1:
        x, y = current
        neighbors = []

        if x > 0:
            neighbors.append((x - 1, y))
        if x < rows - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < cols - 1:
            neighbors.append((x, y + 1))

        found = False
        for nx, ny in neighbors:
            if grid[nx][ny] == current_k - 1:
                path.append((nx, ny))
                current = (nx, ny)
                current_k -= 1
                found = True
                break

        if not found:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    neighbors = []
    if x > 0:
        neighbors.append(grid[x - 1][y])
    if x < rows - 1:
        neighbors.append(grid[x + 1][y])
    if y > 0:
        neighbors.append(grid[x][y - 1])
    if y < cols - 1:
        neighbors.append(grid[x][y + 1])

    wall_count = sum(1 for neighbor in neighbors if neighbor == "■")

    if (x == 0 or x == rows - 1) and (y == 0 or y == cols - 1):
        return wall_count >= 2

    if (x == 0 or x == rows - 1) or (y == 0 or y == cols - 1):
        return wall_count >= 3

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    grid = deepcopy(grid)

    exits = get_exits(grid)

    if len(exits) < 2:
        return grid, exits[0] if exits else None

    if len(exits) == 1:
        return grid, exits[0]

    entrance = exits[0]
    exit_point = exits[1]

    if encircled_exit(grid, exit_point):
        return grid, None

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == " ":
                grid[x][y] = 0
            elif grid[x][y] == "X" and (x, y) == entrance:
                grid[x][y] = 1
            elif grid[x][y] == "X":
                grid[x][y] = 0

    k = 1
    while grid[exit_point[0]][exit_point[1]] == 0:
        grid = make_step(grid, k)
        k += 1
        if k > len(grid) * len(grid[0]):
            return grid, None

    path = shortest_path(grid, exit_point)

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
