import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
                Вернуть список соседних клеток для клетки `cell`.

                Соседними считаются клетки по горизонтали, вертикали и диагоналям,
                то есть, во всех направлениях.

                Parameters
                ----------
                cell : Cell
                    Клетка, для которой необходимо получить список соседей. Клетка
                    представлена кортежем, содержащим ее координаты на игровом поле.

                Returns
                ----------
                out : Cells
                    Список соседних клеток.
                """
        row, col = cell
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbours.append(self.curr_generation[new_row][new_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
                Получить следующее поколение клеток.

                Returns
                ----------
                out : Grid
                    Новое поколение клеток.
                """
        new_grid = self.create_grid(randomize=False)
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbours = self.get_neighbours((row, col))
                live_neighbours = sum(neighbours)
                if self.grid[row][col] == 1:
                    if live_neighbours == 2 or live_neighbours == 3:
                        new_grid[row][col] = 1
                else:
                    if live_neighbours == 3:
                        new_grid[row][col] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1


    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation


    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = f.readlines()
        rows = len(lines)
        cols = len(lines[0].strip())
        game = GameOfLife(size=(rows, cols), randomize=False)
        for row, line in enumerate(lines):
            line = line.strip()
            for col, char in enumerate(line):
                if char == "1":
                    game.curr_generation[row][col] = 1
                else:
                    game.curr_generation[row][col] = 0
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                line = "".join("1" if cell == 1 else "0" for cell in row)
                f.write(line + "\n")
