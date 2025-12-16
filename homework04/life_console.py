import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
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
        """Отобразить состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addch(row + 1, col + 1, "█")
                else:
                    screen.addch(row + 1, col + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        screen.keypad(True)
        screen.timeout(200)
        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                key = screen.getch()
                if key == ord("q"):
                    break
                self.life.step()
        finally:
            curses.curs_set(1)
            curses.nocbreak()
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(15, 40), randomize=True, max_generations=100)
    ui = Console(game)
    ui.run()
