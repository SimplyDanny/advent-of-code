import re

import numpy as np

from common import print_results, readlines


class Display:
    RECT_REGEX = re.compile(r'^rect (\d+)x(\d+)$')
    ROT_ROW_REGEX = re.compile(r'^rotate row y=(\d+) by (\d+)$')
    ROT_COL_REGEX = re.compile(r'^rotate column x=(\d+) by (\d+)$')

    LETTERS = {
        'C': np.array([
                 [0, 1, 1, 0, 0],
                 [1, 0, 0, 1, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0],
             ]),
        'H': np.array([
                 [1, 0, 0, 1, 0],
                 [1, 0, 0, 1, 0],
                 [1, 1, 1, 1, 0],
                 [1, 0, 0, 1, 0],
                 [1, 0, 0, 1, 0],
                 [1, 0, 0, 1, 0],
             ]),
        'J': np.array([
                 [0, 0, 1, 1, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0],
                 [1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0],
             ]),
        'K': np.array([
                 [1, 0, 0, 1, 0],
                 [1, 0, 1, 0, 0],
                 [1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0],
                 [1, 0, 1, 0, 0],
                 [1, 0, 0, 1, 0],
             ]),
        'L': np.array([
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 1, 1, 1, 0],
             ]),
        'P': np.array([
                 [1, 1, 1, 0, 0],
                 [1, 0, 0, 1, 0],
                 [1, 0, 0, 1, 0],
                 [1, 1, 1, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0],
             ]),
        'R': np.array([
                 [1, 1, 1, 0, 0],
                 [1, 0, 0, 1, 0],
                 [1, 0, 0, 1, 0],
                 [1, 1, 1, 0, 0],
                 [1, 0, 1, 0, 0],
                 [1, 0, 0, 1, 0],
             ]),
        'Y': np.array([
                 [1, 0, 0, 0, 1],
                 [1, 0, 0, 0, 1],
                 [0, 1, 0, 1, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
             ]),
        'Z': np.array([
                 [1, 1, 1, 1, 0],
                 [0, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 0],
                 [1, 0, 0, 0, 0],
                 [1, 1, 1, 1, 0],
             ]),
    }

    def __init__(self):
        self.display = np.zeros((6, 50), dtype=int)

    def process_operation(self, operation):
        if operation.startswith('rect'):
            params = map(int, Display.RECT_REGEX.match(operation).groups())
            self.__turn_on_rect(*params)
        elif operation.startswith('rotate row'):
            params = map(int, Display.ROT_ROW_REGEX.match(operation).groups())
            self.__rot_row(*params)
        elif operation.startswith('rotate column'):
            params = map(int, Display.ROT_COL_REGEX.match(operation).groups())
            self.__rot_col(*params)
        else:
            print('Operation \'{}\' not recognized.'.format(operation))

    def __turn_on_rect(self, width, height):
        self.display[:height, :width] = 1

    def __rot_row(self, row, shift):
        self.display[row, :] = np.roll(self.display[row, :], shift)

    def __rot_col(self, column, shift):
        self.display[:, column] = np.roll(self.display[:, column], shift)

    def count_pixels(self):
        return sum(sum(self.display))

    def get_letters(self):
        letters = ''
        for i in range(0, 50, 5):
            for k, v in Display.LETTERS.items():
                if np.array_equal(v, self.display[:, i:i+5]):
                    letters += k
        return letters

#### Main part.

display = Display()
for operation in readlines(__file__):
    display.process_operation(operation)

print_results(display.count_pixels(), display.get_letters())
