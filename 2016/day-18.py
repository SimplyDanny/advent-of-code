from common import print_results, readline


NUMBER_ROWS_1 = 40 - 1
NUMBER_ROWS_2 = 400000 - 1

class Row:
    def __init__(self, repr):
        self.length = len(repr)
        self.boolean_repr = [False] * self.length

    @classmethod
    def from_string(cls, str_repr):
        new_row = Row(str_repr)
        new_row.boolean_repr = list(tile == '.' for tile in str_repr)
        return new_row

    @classmethod
    def from_previous(cls, previous_row):
        new_row = Row(previous_row)
        for i in range(new_row.length):
            right = previous_row[i - 1]
            center = previous_row[i]
            left = previous_row[i + 1]

            new_row[i] = not any((
            # Its left and center tiles are traps, but its right tile is not.
                not left and not center and right,
            # Its center and right tiles are traps, but its left tile is not.
                not center and not right and left,
            # Only its left tile is a trap.
                not left and center and right,
            # Only its right tile is a trap.
                not right and center and left,
            ))

        return new_row

    def get_number_safe_tiles(self):
        return sum(self.boolean_repr)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return True if index in (-1, self.length) else self.boolean_repr[index]

    def __setitem__(self, index, value):
        self.boolean_repr[index] = value

class ApparentField:
    def __init__(self, first_row):
        self.previous_row = first_row
        self.number_safe_tiles = self.previous_row.get_number_safe_tiles()

    def __add_next_row(self):
        new_row = Row.from_previous(self.previous_row)
        self.previous_row = new_row
        self.number_safe_tiles += new_row.get_number_safe_tiles()

    def add_rows(self, number_rows):
        for i in range(number_rows):
            self.__add_next_row()

#### Main part.

first_row = Row.from_string(readline(__file__))

field = ApparentField(first_row)
field.add_rows(NUMBER_ROWS_1)
part_1 = field.number_safe_tiles
field.add_rows(NUMBER_ROWS_2 - NUMBER_ROWS_1)
part_2 = field.number_safe_tiles

print_results(part_1, part_2)
