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
        cell_height, cell_width = self.rows, self.cols
        grid: list[list[int]] = []
        for _ in range(cell_height):
            row = (
                [random.randint(0, 1) for _ in range(cell_width)]
                if randomize == True
                else [0 for _ in range(cell_width)]
            )
            grid.append(row)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        neighbours = []
        for next_x in range(-1, 2):
            for next_y in range(-1, 2):
                if (next_x != 0 or next_y != 0) and 0 <= x + next_x < self.rows and 0 <= y + next_y < self.cols:
                    neighbours.append(self.curr_generation[x + next_x][y + next_y])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_gen = self.create_grid(False)
        for x in range(0, self.rows):
            for y in range(0, self.cols):
                neighbours = self.get_neighbours((x, y))
                if self.curr_generation[x][y] and 2 <= sum(neighbours) <= 3:
                    new_gen[x][y] = 1
                elif not self.curr_generation[x][y] and sum(neighbours) == 3:
                    new_gen[x][y] = 1
        self.generations += 1
        return new_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            return self.generations <= self.max_generations
        return False

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
        with open(filename, encoding="utf-8") as file:
            grid = [list(map(int, line.strip())) for line in file.readlines() if line != "\n"]

        rows = len(grid)
        cols = len(grid[0])
        game_instance = GameOfLife((rows, cols), False)
        game_instance.curr_generation = grid

        return game_instance

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as file:
            for line in self.curr_generation:
                print("".join(map(str, line)), file=file, sep="")
