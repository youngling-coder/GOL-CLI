import time
import os
import sys
import random
import numpy as np
from style import StyleConfig
from cliargs import CLIArg


class ConwaysGameOfLife:
    def __init__(
        self,
        width: int,
        height: int,
        char: chr,
        attach_to_terminal_size: bool = False,
        refill_on_resize: bool = False,
    ) -> None:
        self._width = width
        self._height = height

        self._refill_on_resize = refill_on_resize
        print(refill_on_resize)
        self._is_attached_to_terminal_size = attach_to_terminal_size

        self._char = char

        self._generation = 0

        self._total_births = 0
        self._total_deaths = 0

        self._field = np.zeros((self._height, self._width))
        self._new_frame = self._field.copy()

    def create_state(self):
        for y in range(self._height):
            for x in range(self._width):
                self._field[y, x] = random.randint(0, 1)

    def update_size(self):
        terminal_size = os.get_terminal_size()

        new_height = terminal_size.lines - 3
        new_width = terminal_size.columns - 2
        size_icnreased = False

        if self._is_attached_to_terminal_size or not self._height:
            if new_height > self._height:
                new_rows = np.zeros((new_height - self._height, self._width))
                self._field = np.vstack([self._field, new_rows])
                self._new_frame = np.vstack([self._new_frame, new_rows])
                size_icnreased = True
            elif new_height < self._height:
                self._new_frame = self._new_frame[:new_height]
                self._field = self._field[:new_height]

            self._height = new_height

        if self._is_attached_to_terminal_size or not self._width:
            if new_width > self._width:
                new_cols = np.zeros((self._height, new_width - self._width))
                self._field = np.hstack([self._field, new_cols])
                self._new_frame = np.hstack([self._new_frame, new_cols])
                size_icnreased = True
            elif new_width < self._width:
                self._new_frame = np.delete(
                    self._new_frame, list(range(new_width, self._width)), axis=1
                )
                self._field = np.delete(
                    self._field, list(range(new_width, self._width)), axis=1
                )

            self._width = new_width

        if self._is_attached_to_terminal_size and self._refill_on_resize and size_icnreased:
            self.create_state()


    def stay_alive(self, x: int, y: int):
        area_around = self.get_area_around(x, y)
        amount_of_alive_cells_around = self.count_alive_cells_in_area(area_around)

        if self._field[y, x] == 0:
            if amount_of_alive_cells_around == 3:
                self._new_frame[y, x] = 1
            else:
                self._new_frame[y, x] = 0
        else:
            amount_of_alive_cells_around -= 1
            if amount_of_alive_cells_around < 2 or amount_of_alive_cells_around > 3:
                self._new_frame[y, x] = 0
            else:
                self._new_frame[y, x] = 1

    def count_alive_cells_in_area(self, area: np.array):

        count = np.count_nonzero(area)

        return count if not count else count

    def get_area_around(self, x: int, y: int):
        """
        Calculates and returns 2D slice of the field around the cells with X and Y coordinates
        :param int x: X coordinate of the target cell
        :param int y: Y coordinate of the target cell
        :rtype: None
        """

        # Set default values for indexes, supposing X and Y don't have minimum or maximum values
        x_subarea_indexes = [x - 1, x, x + 1]
        y_subarea_indexes = [y - 1, y, y + 1]

        # If any of the conditions are not satisfied, set new X indexes
        if x == 0:
            x_subarea_indexes = [self._width - 1, x, x + 1]
        elif x == self._width - 1:
            x_subarea_indexes = [self._width - 2, self._width - 1, 0]

        # The same with Y indexes
        if y == 0:
            y_subarea_indexes = [self._height - 1, y, y + 1]
        elif y == self._height - 1:
            y_subarea_indexes = [self._height - 2, self._height - 1, 0]

        # Selecting values that are in range of X and Y indexes
        sub_area = self._field[np.ix_(y_subarea_indexes, x_subarea_indexes)]

        return sub_area

    def draw_field(self):
        additional = int(not (self._width % 2))
        frame_str = (
            "╭"
            + "─" * int((self._width - 23) / 2)
            + " Conway's Game Of Life "
            + "─" * (int((self._width - 23) / 2) + additional)
            + "╮\n"
        )

        for y in range(self._height):
            frame_str += f"{StyleConfig.BorderColor + StyleConfig.FontStyle}│{StyleConfig.ResetAll}"
            for x in range(self._width):
                if not self._new_frame[y, x]:
                    frame_str += " "
                else:
                    frame_str += f"{StyleConfig.AliveColor + StyleConfig.FontStyle + StyleConfig.BackgroundColor}{self._char}"
            frame_str += f"{StyleConfig.ResetAll + StyleConfig.BorderColor + StyleConfig.FontStyle + StyleConfig.BackgroundColor}│\n"
        frame_str += "╰" + "─" * self._width + "╯"
        print(frame_str)

    @staticmethod
    def show_help():
        help_msg = f"""
  {StyleConfig.FontStyle}{StyleConfig.BorderColor}  Welcome to Conway's Game Of Life!
    {StyleConfig.AliveColor}
    -h\t 󰜴 \tShow this message, discards program start

    -H\t 󰜴 \tSet default height (0 value will be overrided by terminal height)
    -W\t 󰜴 \tSet default width (0 value will be overrided by terminal width)
    -c\t 󰜴 \tUse custom character for a cell (default is '')
    -t\t 󰜴 \tUse terminal size (overrides -H and -W)
    -r\t 󰜴 \tRefill the field on resize (work when -t flag specified)"""
        print(help_msg)

    def run(self):
        self.create_state()
        while True:
            self.update_size()
            self.draw_field()

            for y in range(self._height):
                for x in range(self._width):
                    self.stay_alive(x, y)

            self._field =  self._new_frame.copy()

            time.sleep(0.2)
            os.system("clear")


if __name__ == "__main__":
    args = sys.orig_argv
    print(args)
    height = 0
    width = 0
    char = ""
    attach_to_terminal_size = False
    refill_on_resize = False

    if "-h" in args:
        ConwaysGameOfLife.show_help()
    else:
        for i in range(1, len(args)):
            if args[i] == CLIArg.Height:
                height = int(args[i + 1])
            elif args[i] == CLIArg.Width:
                width = int(args[i + 1])
            elif args[i] == CLIArg.Character:
                char = args[i + 1]
            elif args[i] == CLIArg.TerminalSize:
                attach_to_terminal_size = True
            elif args[i] == CLIArg.RefillOnResize:
                refill_on_resize = True

        game = ConwaysGameOfLife(
            width=width,
            height=height,
            char=char,
            attach_to_terminal_size=attach_to_terminal_size,
            refill_on_resize=refill_on_resize,
        )

        game.update_size()
        game.run()
