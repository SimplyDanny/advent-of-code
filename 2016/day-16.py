from common import print_results, readline


INITIAL_STATE = readline(__file__)
DISK_LENGTH_1 = 272
DISK_LENGTH_2 = 35651584

class BinaryNumber:
    def __init__(self, binary_number_string):
        self.str_repr = binary_number_string

    def __str__(self):
        return self.str_repr

    def __len__(self):
        return len(self.str_repr)

    def __neg__(self):
        return BinaryNumber(self.str_repr[::-1])

    def __invert__(self):
        return BinaryNumber(
            ''.join('1' if x is '0' else '0' for x in self.str_repr)
        )

    def __iadd__(self, other):
        self.str_repr += '0' + other.str_repr
        return self

    def __getitem__(self, items):
        return self.str_repr[items]

def generate_data(initial_data, length):
    a = BinaryNumber(initial_data)
    while len(a) < length:
        a += ~-a
    return a[:length]

def compute_checksum(binary_number_string):
    pairs = list(
        binary_number_string[i:i+2]
        for i in range(0, len(binary_number_string), 2)
    )
    properties_of_pairs = list('1' if p[0] == p[1] else '0' for p in pairs)
    checksum = ''.join(properties_of_pairs)
    return checksum if len(checksum) % 2 != 0 else compute_checksum(checksum)

#### Main part.

print_results(
    compute_checksum(generate_data(INITIAL_STATE, DISK_LENGTH_1)),
    compute_checksum(generate_data(INITIAL_STATE, DISK_LENGTH_2))
)
