import re

from numpy import product

from common import print_results, readlines


class Factory:
    BOT_REGEX = re.compile(
        r'^bot (?P<number>\d+) gives '
        r'low to (?P<low_kind>bot|output) (?P<low_number>\d+) and '
        r'high to (?P<high_kind>bot|output) (?P<high_number>\d+)$'
    )
    VALUE_REGEX = re.compile(
        r'^value (?P<value>\d+) goes to bot (?P<number>\d+)$'
    )

    def __init__(self):
        self.bots = {}
        self.outputs = {}

    def add(self, instruction):
        if instruction.startswith('bot'):
            m = Factory.BOT_REGEX.match(line)
            self.__handle_bot_instruction(
                int(m.group('number')),
                m.group('low_kind'),
                int(m.group('low_number')),
                m.group('high_kind'),
                int(m.group('high_number')),
            )
        elif instruction.startswith('value'):
            m = Factory.VALUE_REGEX.match(instruction)
            self.__handle_value_instruction(
                int(m.group('number')),
                int(m.group('value')),
            )
        else:
            raise ValueError('Instruction line not recognized.')

    def __handle_value_instruction(self, number, value):
        if number in self.bots:
            self.bots[number].add_value(value)
        else:
            self.bots[number] = Bot.with_value(number, value)

    def __handle_bot_instruction(self, number, low_kind, low_number,
                                 high_kind, high_number):
        if number in self.bots:
            self.bots[number].low_to = (low_number, low_kind)
            self.bots[number].high_to = (high_number, high_kind)
        else:
            self.bots[number] = Bot.with_destinations(
                number,
                (low_number, low_kind),
                (high_number, high_kind),
            )

        self.__add_to_appropriate(low_kind, low_number)
        self.__add_to_appropriate(high_kind, high_number)

    def __add_to_appropriate(self, kind, number):
        if kind == 'bot' and number not in self.bots:
            self.bots[number] = Bot(number)
        elif kind == 'output' and number not in self.outputs:
            self.outputs[number] = Output(number)

    def __run_bot(self, bot):
        if bot.is_prepared():
            exec('self.' +
                 bot.low_to[1] +
                 's[bot.low_to[0]].add_value(bot.values[0])')
            exec('self.' +
                 bot.high_to[1] +
                 's[bot.high_to[0]].add_value(bot.values[1])')
            bot.handled = True

    def run(self):
        while True:
            all_bots_handled = True
            for bot in self.bots.values():
                all_bots_handled &= bot.handled
                self.__run_bot(bot)
            if all_bots_handled:
                break

    def get_bot_which_handles(self, values):
        for number, bot in self.bots.items():
            if bot.values == values:
                return number
        else:
            return 'No bot is responsible for the given pair of values.'

    def get_multiplied_outputs(self, numbers):
        return product([self.outputs[number].get_sum() for number in numbers])

class Bot:
    def __init__(self, number):
        self.number = number
        self.values = []
        self.low_to = None
        self.high_to = None
        self.handled = False

    @classmethod
    def with_destinations(cls, number, low_to, high_to):
        bot = cls(number)
        bot.low_to = low_to
        bot.high_to = high_to
        return bot

    @classmethod
    def with_value(cls, number, value):
        bot = cls(number)
        bot.values.append(value)
        return bot

    def add_value(self, value):
        if not self.handled:
            self.values.append(value)
            self.values.sort()

    def is_prepared(self):
        return (
            not self.handled
            and self.low_to is not None
            and self.high_to is not None
            and len(self.values) == 2
        )

class Output:
    def __init__(self, number):
        self.number = number
        self.values = set()

    def add_value(self, value):
        self.values.add(value)

    def get_sum(self):
        return sum(self.values)

#### Main part.

factory = Factory()

for line in readlines(__file__):
    factory.add(line)

factory.run()

print_results(
    factory.get_bot_which_handles([17, 61]),
    factory.get_multiplied_outputs([0, 1, 2])
)
