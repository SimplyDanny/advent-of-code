import re

from common import print_results, readlines


ADDITIONAL_DISC = (11, 0)

REGEX_INPUT = re.compile(
    r'^Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+).$'
)

def positions_of_discs(time, discs):
    return map(
        lambda t: (t[1][1] + time + t[0]) % t[1][0],
        enumerate(discs, start=1)
    )

def first_possible_start_time(discs, start_time=0):
    time = start_time
    while True:
        if sum(positions_of_discs(time, discs)) == 0:
            return time
        time += 1

#### Main part.

discs = list(map(
    lambda line: tuple(map(int, REGEX_INPUT.match(line).groups())),
    readlines(__file__)
))

part_1 = first_possible_start_time(discs)
part_2 = first_possible_start_time(discs + [ADDITIONAL_DISC], start_time=part_1)

print_results(part_1, part_2)
