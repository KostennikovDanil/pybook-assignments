import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode(
            (self.life.cols * self.cell_size, self.life.rows * self.cell_size)
        )

    def draw_lines(self) -> None:

        width = self.life.cols * self.cell_size
        height = self.life.rows * self.cell_size
        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (width, y))

    def draw_grid(self) -> None:

        lenght = self.cell_size - 1
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                pygame.draw.rect(
                    self.screen,
                    color,
                    (i * self.cell_size + 1, j * self.cell_size + 1, lenght, lenght),
                )

    def run(self) -> None:

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = True

            self.draw_lines()

            if pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        pause = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        doc = event.pos
                        row = doc[1] // self.cell_size
                        col = doc[0] // self.cell_size
                        if self.life.curr_generation[row][col]:
                            self.life.curr_generation[row][col] = 0
                        else:
                            self.life.curr_generation[row][col] = 1
                        self.draw_grid()
                        pygame.display.flip()
            else:

                self.life.step()
                self.draw_grid()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((20, 20), max_generations=500)
    gui = GUI(life)
    gui.run()
