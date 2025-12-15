import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addch(0, 0, "+")
        screen.addch(0, self.life.cols + 1, "+")
        screen.addch(self.life.rows + 1, 0, "+")
        screen.addch(self.life.rows + 1, self.life.cols + 1, "+")
        for x in range(1, self.life.cols + 1):
            screen.addch(0, x, "-")
            screen.addch(self.life.rows + 1, x, "-")
        for y in range(1, self.life.rows + 1):
            screen.addch(y, 0, "|")
            screen.addch(y, self.life.cols + 1, "|")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addch(row + 1, col + 1, "█")
                else:
                    screen.addch(row + 1, col + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.endwin()
