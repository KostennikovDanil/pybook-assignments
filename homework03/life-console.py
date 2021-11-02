import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """

        screen.clear()
        y, x = screen.getmaxyx()
        doc = ""

        for row in range(y):
            for col in range(x):
                if row == 0 or row == (y - 1):
                    if col == 0 or col == x:
                        doc += "*"
                    else:
                        doc += "-"
                elif row < (y - 1) and row > 0:
                    if col == 0 or col == (x - 1):
                        doc += "|"
                    else:
                        doc += " "
            try:
                screen.addstr(doc)
            except curses.error:
                pass
            doc = ""

        self.draw_grid(screen)
        screen.refresh()
        screen.getch()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """

        y, x = screen.getmaxyx()
        col = (x - self.life.cols) // 2
        row = (y - self.life.rows) // 2
        for count_row, just_row in enumerate(self.life.curr_generation):
            for count_col, just_col in enumerate(just_row):
                if just_col:
                    try:
                        screen.addstr(count_row + row, count_col + col, "*")
                    except curses.error:
                        pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.wrapper(self.draw_borders)
        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.life.step()
            self.draw_borders(screen)
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=50)
    gui = Console(life)
    gui.run()
