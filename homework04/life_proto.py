import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        cell_height, cell_width = self.cell_height, self.cell_width
        grid: list[list[int]] = []
        for _ in range(cell_height):
            row = (
                [random.randint(0, 1) for _ in range(cell_width)]
                if randomize == True
                else [0 for _ in range(cell_width)]
            )
            grid.append(row)

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        surface = self.screen
        for row_number, row in enumerate(self.grid):
            for col_number, cell in enumerate(row):
                color = "green" if cell == 1 else "white"
                rect = (row_number * self.cell_height, col_number * self.cell_width, self.cell_height, self.cell_width)
                pygame.draw.rect(surface, color, rect)

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
        x, y = cell
        neighbours = []
        for next_x in range(-1, 2):
            for next_y in range(-1, 2):
                if (
                    (next_x != 0 or next_y != 0)
                    and 0 <= x + next_x < self.cell_height
                    and 0 <= y + next_y < self.cell_width
                ):
                    neighbours.append(self.grid[x + next_x][y + next_y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid(False)
        for x in range(0, self.cell_height):
            for y in range(0, self.cell_width):
                neighbours = self.get_neighbours((x, y))
                if self.grid[x][y] and 2 <= sum(neighbours) <= 3:
                    new_grid[x][y] = 1
                elif not self.grid[x][y] and sum(neighbours) == 3:
                    new_grid[x][y] = 1
        return new_grid
