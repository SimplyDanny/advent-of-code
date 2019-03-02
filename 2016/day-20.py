import re
from collections import deque, namedtuple

from common import print_results, readlines


NUMBER_IP_ADDRESSES = 2**32

REGEX_RANGE = re.compile(r'^(\d+)-(\d+)$')

IPInterval = namedtuple('IPInterval', 'start end')

def get_smallest_possible(intervals):
    smallest_ip = 0
    start, end = intervals.popleft()
    while start <= smallest_ip:
        smallest_ip = end + 1
        start, end = intervals.popleft()
    return smallest_ip

def count_all_possible(intervals):
    counter, possible_white_ip = 0, 0
    while len(intervals) > 0:
        start, end = intervals.popleft()
        counter += max(0, start - possible_white_ip)
        possible_white_ip = max(end + 1, possible_white_ip)
    return counter + NUMBER_IP_ADDRESSES - possible_white_ip

#### Main part.

intervals = sorted(
    (IPInterval(*map(int, REGEX_RANGE.match(line).groups()))
    for line in readlines(__file__)),
    key=lambda interval: interval.start
)

print_results(
    get_smallest_possible(deque(intervals)),
    count_all_possible(deque(intervals))
)
