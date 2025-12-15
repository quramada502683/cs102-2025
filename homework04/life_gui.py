import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.paused = False

    def draw_lines(self) -> None:
        # Copy from previous assignment
        pass

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                x = col * self.cell_size
                y = row * self.cell_size
                width = self.cell_size
                height = self.cell_size
                pygame.draw.rect(self.screen, color, (x, y, width, height))

    def run(self) -> None:
        # Copy from previous assignment
        pass
