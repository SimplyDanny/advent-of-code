import re

import numpy as np

from common import print_results, read


INSTRUCTION_REGEX = re.compile(r'(L|R)(\d+)')

class Path:
    # Announce two rotation matrices which will bring the update vectors from
    # input into the right direction according to the previous step made. The
    # matrix 'self.rotation' represents the actual overall rotation. An input
    # of the form 'Rr' will be interpreted as the vector '(r, 0)' while 'Ll'
    # coincides with '(-l, 0)'.
    R = np.array([
        [0, -1],
        [1,  0]
    ])
    L = np.array([
        [ 0, 1],
        [-1, 0]
    ])

    def __init__(self):
        self.rotation = np.array([
            [1, 0],
            [0, 1]
        ])
        self.position = np.array([0, 0])
        self.bookmarks = [np.copy(self.position)]
        self.visitedLocationTwice = False

    def update_position(self, direction, width):
        width = int(width)
        if direction == 'R':
            widths = [np.array([i, 0]) for i in range(1, width + 1)]
            self.__bookmark_path(widths)
            self.rotation = self.rotation.dot(self.R)
        elif direction == 'L':
            widths = [np.array([-i, 0]) for i in range(1, width + 1)]
            self.__bookmark_path(widths)
            self.rotation = self.rotation.dot(self.L)

    def __bookmark_path(self, widths):
        for w in widths:
            position = self.position + w.dot(self.rotation)
            if not self.visitedLocationTwice:
                self.__is_position_bookmarked(position)
            self.bookmarks.append(np.copy(position))
        self.position = self.bookmarks[-1]

    def __is_position_bookmarked(self, position):
        if any((position == p).all() for p in self.bookmarks):
            self.firstVisitedTwice = np.copy(position)
            self.visitedLocationTwice = True

    @staticmethod
    def get_manhattan_distance(point):
        return sum(map(abs, point))

#### Main part.

instructions = [
    m.groups() for m in map(INSTRUCTION_REGEX.match, read(__file__).split(', '))
]

path = Path()
for instruction in instructions:
    path.update_position(*instruction)

print_results(
    Path.get_manhattan_distance(path.position),
    Path.get_manhattan_distance(path.firstVisitedTwice)
)
