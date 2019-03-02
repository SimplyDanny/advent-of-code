import re
from collections import OrderedDict
from string import ascii_lowercase

from common import print_results, readlines


NORTHPOLE_OBJECT_STORAGE = 'northpole object storage'

class Room:
    ROOM_REGEX = re.compile(r'^([\w-]+)-(\d+)\[(\w+)\]$')

    LETTERS = list(ascii_lowercase)
    DIGITS = list(range(26))

    DIGIT_TO_LETTER = dict(zip(DIGITS, LETTERS))
    DIGIT_TO_LETTER[' '] = ' '

    LETTER_TO_DIGIT = dict((v, k) for k, v in DIGIT_TO_LETTER.items())
    LETTER_TO_DIGIT['-'] = ' '

    def __init__(self, line):
        m = self.ROOM_REGEX.match(line)

        self.name = m.group(1)
        self.id = int(m.group(2))
        self.checksum = m.group(3)
        self.name_length = len(self.name)

        # For all letters count their number of occurrence in the room name.
        self.letter_counter = {
            letter: self.name.count(letter) for letter in self.LETTERS
        }

        # Convert name into digit representation.
        self.name_in_digit_representation = [
            self.LETTER_TO_DIGIT[letter] for letter in list(self.name)
        ]

    def get_sector_id_if_real(self):
        return (self.checksum == self.__get_real_checksum()) * self.id

    def __get_real_checksum(self):
        # Collect letters in lists which have the same number of occurrence in
        # the room name. The 'filter' removes empty lists in case there are no
        # letters with the according number of occurrence.
        letters_sorted_by_number_of_occurrence = list(filter(([]).__ne__, [
            [
                letter
                for letter in self.letter_counter
                if self.letter_counter[letter] == i
            ]
            for i in range(self.name_length, 0, -1)
        ]))

        # First sort all lists in 'letters_sorted_by_number_of_occurrence' in
        # alphabetical order and join them to one string. Then join them all
        # together to get one long string with all occuring letters in the order
        # given by the checksum rule.
        letters_in_checksum_order = ''.join(
            ''.join(sorted(letters))
            for letters in letters_sorted_by_number_of_occurrence
        )

        # Return the first 5 to get the checksum.
        return letters_in_checksum_order[:5]

    def get_id_of_room(self, name):
        for i in range(self.name_length):
            if self.name_in_digit_representation[i] != ' ':
                self.name_in_digit_representation[i] += self.id
                self.name_in_digit_representation[i] %= 26
        decrypted_name = ''.join([
            self.DIGIT_TO_LETTER[d] for d in self.name_in_digit_representation
        ])
        return self.id if decrypted_name == name else 0

#### Main part.

rooms = [Room(line) for line in readlines(__file__)]

# Part One
sum_of_ids = sum(room.get_sector_id_if_real() for room in rooms)

# Part Two
northpole_object_storage_id = sum(
    room.get_id_of_room(NORTHPOLE_OBJECT_STORAGE) for room in rooms
)

print_results(sum_of_ids, northpole_object_storage_id)
