import hashlib
import re

from common import print_results, readline


SALT = readline(__file__)
REACHABLE_NUMBER = 1000
TO_FIND = 64
TIMES = 2016 + 1

class PossibleKey:
    REGEX_THREE = re.compile(r'(.)\1{2}')
    REGEX_FIVE = re.compile(r'(.)\1{4}')

    def __init__(self, md5):
        try:
            self.three_char, = PossibleKey.REGEX_THREE.search(md5).groups()
            self.five_chars = PossibleKey.REGEX_FIVE.findall(md5)
        except AttributeError:
            self.three_char = ' '
            self.five_chars = []

    @classmethod
    def generate_key(cls, times):
        suffix = 0
        while True:
            to_hash = SALT + str(suffix)
            for _ in range(times):
                to_hash = hashlib.md5(str.encode(to_hash)).hexdigest()
            yield cls(to_hash), suffix
            suffix += 1

class KeyFinder:
    def __init__(self, times_to_hash=1):
        self.occurred_triples = []
        self.times_to_hash = times_to_hash
        self.one_time_pad_key_counter = 0

    @property
    def reachable_triple(self):
        return self.occurred_triples[-1000:-1]

    def pos_in_reachable_triple(self, char):
        try:
            return self.reachable_triple.index(char)
        except ValueError:
            return -1

    def remove_reachable_triple(self, index):
        length = len(self.occurred_triples)
        index += (length - REACHABLE_NUMBER) * (length > 1000)
        self.occurred_triples[index] = ' '

    def get_index(self):
        for possible_key, i in PossibleKey.generate_key(self.times_to_hash):
            self.occurred_triples.append(possible_key.three_char)
            for five_char in possible_key.five_chars:
                while True:
                    first_occurrence = self.pos_in_reachable_triple(five_char)
                    if first_occurrence == -1: break
                    self.one_time_pad_key_counter += 1
                    self.remove_reachable_triple(first_occurrence)
                    if self.one_time_pad_key_counter == TO_FIND:
                        return self.__compute_number(i, first_occurrence)

    def __compute_number(self, i, j):
        return i - 999 + j

#### Main Part.

print_results(KeyFinder(1).get_index(), KeyFinder(TIMES).get_index())
