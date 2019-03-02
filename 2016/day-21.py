import re

from common import print_results, readlines


STRING_PART_1 = 'abcdefgh'
STRING_PART_2 = 'fbgdceah'

class Scrambler:
    PATTERN_TO_METHOD = {
        re.compile(r'swap position (\d) with position (\d)'):   'swap_position',
        re.compile(r'swap letter (\w) with letter (\w)'):       'swap_letter',
        re.compile(r'rotate (left|right) (\d) steps?'):         'rotate_dir',
        re.compile(r'rotate based on position of letter (\w)'): 'rotate_pos',
        re.compile(r'reverse positions (\d) through (\d)'):     'reverse',
        re.compile(r'move position (\d) to position (\d)'):     'move',
    }

    def __init__(self, initial_password):
        self.passwort = list(initial_password)

    def scramble(self, rule):
        for pattern, method_name in Scrambler.PATTERN_TO_METHOD.items():
            match = pattern.match(rule)
            if match is not None:
                exec('self.' + method_name + '(*match.groups())')
                return

    def swap_position(self, x, y):
        x, y = int(x), int(y)
        self.passwort[x], self.passwort[y] = self.passwort[y], self.passwort[x]

    def swap_letter(self, letter_1, letter_2):
        index_letter_1 = self.passwort.index(letter_1)
        index_letter_2 = self.passwort.index(letter_2)
        self.passwort[index_letter_1] = letter_2
        self.passwort[index_letter_2] = letter_1

    def rotate_dir(self, dir, steps):
        steps = (int(steps) if dir == 'left' else -int(steps)) % 8
        self.passwort = self.passwort[steps:] + self.passwort[:steps]

    def rotate_pos(self, letter):
        index = self.passwort.index(letter)
        self.rotate_dir('right', 1 + index + (index >= 4))

    def reverse(self, x, y):
        x, y = int(x), int(y) + 1
        self.passwort[x:y] = reversed(self.passwort[x:y])

    def move(self, x, y):
        self.passwort.insert(int(y), self.passwort.pop(int(x)))

    def get_password(self):
        return ''.join(self.passwort)

class ReversedScrambler(Scrambler):
    INVERSE_ROTATE_POS_TABLE = [(1 + 2 * i + (i >= 4)) % 8 for i in range(8)]

    def rotate_dir(self, dir, steps):
        super().rotate_dir('right' if dir == 'left' else 'left', steps)

    def rotate_pos(self, letter):
        index = self.passwort.index(letter)
        diff = index - ReversedScrambler.INVERSE_ROTATE_POS_TABLE.index(index)
        super().rotate_dir('left', diff if diff >= 0 else 8 + diff)

    def move(self, x, y):
        super().move(y, x)

#### Main part.

rules = readlines(__file__)

scrambler = Scrambler(STRING_PART_1)
reversed_scrambler = ReversedScrambler(STRING_PART_2)
for i in range(len(rules)):
    scrambler.scramble(rules[i])
    reversed_scrambler.scramble(rules[-i - 1])

print_results(scrambler.get_password(), reversed_scrambler.get_password())
