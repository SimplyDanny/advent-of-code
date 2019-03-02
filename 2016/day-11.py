from collections import OrderedDict, deque, namedtuple
from itertools import chain, combinations
from operator import gt, lt
from re import compile

from common import print_results, readlines


FLOORS = 4

GENERATOR_REGEX = compile(r'([a-z]+) generator')
MICROCHIP_REGEX = compile(r'([a-z]+)-compatible microchip')

Step = namedtuple('Step', ['items', 'direction'])

# Map elements to integers for faster evaluation. Use positive numbers for
# generators and negative numbers for microchips later on.
ELEMENTS = {
    'curium',
    'dilithium',
    'elerium',
    'hydrogen',
    'lithium',
    'plutonium',
    'ruthenium',
    'strontium',
    'thulium',
}
ELEMENT_MAPPING = {v: k for k, v in enumerate(ELEMENTS, start=1)}

class Facility:

    def __init__(self, items, steps=0, elevator=0):
        self.items = items
        self.steps = steps
        self.elevator = elevator

    @classmethod
    def from_input(cls):
        items = OrderedDict()
        for floor, line in enumerate(readlines(__file__)):
            for element in GENERATOR_REGEX.findall(line):
                items[ELEMENT_MAPPING[element]] = floor
            for element in MICROCHIP_REGEX.findall(line):
                items[-ELEMENT_MAPPING[element]] = floor
        return cls(items)

    def __hash__(self):
        return hash((self.elevator, *self.items.values()))

    def get_items_on_floor(self, floor_number):
        return {
            item
            for item, floor in self.items.items()
            if floor == floor_number
        }

    def get_possible_steps(self):
        return [
            Step(items, direction)
            for items in get_max_two(self.get_items_on_floor(self.elevator))
            for direction in (+1, -1)
            if 0 <= self.elevator + direction < FLOORS
        ]

    def get_items_of_type_on_floor(self, predicate, floor_number):
        return {
            item
            for item in self.get_items_on_floor(floor_number)
            if predicate(item, 0)
        }

    def is_consistent(self):
        consistent = True
        for floor in range(FLOORS):
            microchips = self.get_items_of_type_on_floor(lt, floor)
            generators = self.get_items_of_type_on_floor(gt, floor)
            microchips_not_alone = all(
                any(
                    are_compatible(generator, microchip)
                    for generator in generators
                )
                for microchip in microchips
            )
            consistent &= microchips_not_alone or all(
                any(
                    are_compatible(generator, microchip)
                    for microchip in microchips
                )
                for generator in generators
            )
        return consistent

    def copy_applying_step(self, step):
        return Facility(
            {
                item: floor + (item in step.items)*step.direction
                for item, floor in self.items.items()
            },
            self.steps + 1,
            self.elevator + step.direction
        )

    def are_all_on_destination_floor(self):
        return all(floor == FLOORS - 1 for floor in self.items.values())

def get_max_two(iterable):
    return chain(combinations(iterable, 2), combinations(iterable, 1))

def are_compatible(first_item, second_item):
    return not first_item + second_item

def get_minimum_steps(start_facility):
    states = deque([start_facility])
    seen = {hash(start_facility)}
    while states:
        facility = states.pop()
        if facility.are_all_on_destination_floor():
            return facility
        for step in facility.get_possible_steps():
            new_facility = facility.copy_applying_step(step)
            new_facility_hash = hash(new_facility)
            if new_facility_hash not in seen and new_facility.is_consistent():
                states.appendleft(new_facility)
                seen.add(new_facility_hash)

#### Main part.

facility_part_two = Facility.from_input()
facility_part_two.items[ELEMENT_MAPPING['elerium']] = 0
facility_part_two.items[-ELEMENT_MAPPING['elerium']] = 0
facility_part_two.items[ELEMENT_MAPPING['dilithium']] = 0
facility_part_two.items[-ELEMENT_MAPPING['dilithium']] = 0

print_results(
    get_minimum_steps(Facility.from_input()).steps,
    get_minimum_steps(facility_part_two).steps
)
