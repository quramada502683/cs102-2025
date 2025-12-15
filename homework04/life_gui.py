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
        """Отрисовать сетку."""
        for x in range(0, self.width + 1, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height), 1)
        for y in range(0, self.height + 1, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y), 1)

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
        """Запустить игру."""
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.paused = not self.paused
                        print(f"Пауза: {'ВКЛ' if self.paused else 'ВЫКЛ'}")
                elif event.type == MOUSEBUTTONDOWN:
                    if self.paused and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        col = mouse_x // self.cell_size
                        row = mouse_y // self.cell_size
                        if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                            if self.life.curr_generation[row][col] == 1:
                                self.life.curr_generation[row][col] = 0
                                print(f"Убили клетку ({row}, {col})")
                            else:
                                self.life.curr_generation[row][col] = 1
                                print(f"Оживили клетку ({row}, {col})")
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            if not self.paused:
                self.life.step()
                if self.life.is_max_generations_exceeded:
                    print(f"Игра окончена! Достигнут максимум: {self.life.max_generations}")
                    running = False
                elif not self.life.is_changing:
                    print("Игра окончена! Поле стабилизировалось.")
                    running = False
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        print("Игра завершена.")
