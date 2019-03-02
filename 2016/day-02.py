import numpy as np

from common import print_results, readlines


class Keypad:
    DIRECTION_TO_VECTOR = {
        'U': np.array(( 0,  1)),
        'R': np.array(( 1,  0)),
        'D': np.array(( 0, -1)),
        'L': np.array((-1,  0))
    }

    def __init__(self):
        self.key = np.array((0, 0))

    def get_key(self, directions):
        for direction in directions:
            update = self.DIRECTION_TO_VECTOR[direction]
            if tuple(self.key + update) in self.POSITION_TO_KEY.keys():
                self.key += update
        return self.POSITION_TO_KEY[tuple(self.key)]

class KeypadPartOne(Keypad):
    POSITION_TO_KEY = {
        (-1,  1): '1',
        ( 0,  1): '2',
        ( 1,  1): '3',
        (-1,  0): '4',
        ( 0,  0): '5',
        ( 1,  0): '6',
        (-1, -1): '7',
        ( 0, -1): '8',
        ( 1, -1): '9'
    }

class KeypadPartTwo(Keypad):
    POSITION_TO_KEY = {
        (2,  2): '1',
        (1,  1): '2',
        (2,  1): '3',
        (3,  1): '4',
        (0,  0): '5',
        (1,  0): '6',
        (2,  0): '7',
        (3,  0): '8',
        (4,  0): '9',
        (1, -1): 'A',
        (2, -1): 'B',
        (3, -1): 'C',
        (2, -2): 'D'
    }

#### Main part.

instructions = [' '.join(line).split() for line in readlines(__file__)]

print_results(
    ''.join(KeypadPartOne().get_key(dirs) for dirs in instructions),
    ''.join(KeypadPartTwo().get_key(dirs) for dirs in instructions)
)
