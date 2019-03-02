import re

from common import print_results, readline


MARKER_REGEX = re.compile(r'^(\d+)x(\d+)')

def get_length(sequence, version_two=False):
    pos = 0
    counter = 0
    end_pos = len(sequence)
    while pos < end_pos:
        if sequence[pos] is '(':
            number, factor = MARKER_REGEX.match(sequence[pos+1:]).groups()
            marker_length = 1 + len(number) + 1 + len(factor) + 1
            if version_two:
                sub_sequence = sequence[
                    pos + marker_length : pos + marker_length + int(number)
                ]
                counter += int(factor) * get_length(sub_sequence,
                                                    version_two=True)
            else:
                counter += int(number) * int(factor)
            pos += marker_length + int(number)
        else:
            counter += 1
            pos += 1
    return counter

#### Main part.

sequence = readline(__file__)

print_results(get_length(sequence), get_length(sequence, version_two=True))
