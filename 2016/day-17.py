from collections import deque, namedtuple
from hashlib import md5

from common import print_results, readline


INPUT = readline(__file__).encode()

Direction = namedtuple('Direction', ['dx', 'dy', 'token'])

UP      = Direction( 0, -1, b'U')
DOWN    = Direction( 0, +1, b'D')
LEFT    = Direction(-1,  0, b'L')
RIGHT   = Direction(+1,  0, b'R')

class Position:
    def __init__(self, x=0, y=0, tokens=b''):
        self.x = x
        self.y = y
        self.digest = Digest(tokens)

    def get_possible_directions(self):
        up, down, left, right = self.digest.md5[:4]
        directions = []
        if self.x != 0 and Position.is_door_open(left):
            directions.append(LEFT)
        if self.x != 3 and Position.is_door_open(right):
            directions.append(RIGHT)
        if self.y != 0 and Position.is_door_open(up):
            directions.append(UP)
        if self.y != 3 and Position.is_door_open(down):
            directions.append(DOWN)
        return directions

    @staticmethod
    def is_door_open(door):
        return door in 'bcdef'

    def move(self, direction):
        return Position(
            self.x + direction.dx,
            self.y + direction.dy,
            self.digest.message + direction.token
        )

    def is_destination(self):
        return self.x == self.y == 3

class Digest:
    def __init__(self, message):
        self.message = message

    @property
    def md5(self):
        return md5(INPUT + self.message).hexdigest()

    @property
    def message_as_string(self):
        return str(self.message, 'utf-8')

    @property
    def message_length(self):
        return len(self.message)

def find_shortest_path(positions=[Position()]):
    next_positions = []
    for position in positions:
        for direction in position.get_possible_directions():
            next_position = position.move(direction)
            if next_position.is_destination():
                return next_position.digest.message_as_string
            next_positions.append(next_position)
    return find_shortest_path(next_positions)

def find_steps_of_longest_path():
    max_steps = 0
    positions = deque([Position()])
    while positions:
        position = positions.popleft()
        directions = position.get_possible_directions()
        if position.is_destination():
            max_steps = max(position.digest.message_length, max_steps)
        else:
            positions.extend(position.move(d) for d in directions)
    return max_steps

#### Main part.

print_results(find_shortest_path(), find_steps_of_longest_path())
