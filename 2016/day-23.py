from copy import deepcopy
from importlib import import_module

from common import print_results, readlines

day_12 = import_module("day-12")
Program = day_12.Program
Instruction = day_12.Instruction


COMMAND_TOGGLING = {
    'inc': 'dec',
    'dec': 'inc',
    'tgl': 'inc',
    'jnz': 'cpy',
    'cpy': 'jnz',
}

class ExtendedProgram(Program):
    def __init__(self, instructions, register_a_start=0):
        super().__init__(instructions)
        self.reg['a'] = register_a_start
        self.commands['tgl'] = self.command_tgl

    def command_cpy(self, arg1, arg2):
        if arg2.lstrip('-').isdigit():
            self.position += 1
            return
        super().command_cpy(arg1, arg2)

    def command_tgl(self, arg1, arg2):
        position_to_toggle = self.position + self.get_value(arg1)
        self.position += 1
        if not 0 <= position_to_toggle < self.number_instructions:
            return
        instruction = self.instructions[position_to_toggle]
        instruction.command = COMMAND_TOGGLING[instruction.command]

if __name__ == '__main__':
    instructions = [Instruction(*line.split()) for line in readlines(__file__)]

    print_results(
        ExtendedProgram(deepcopy(instructions), 7).run(),
        ExtendedProgram(deepcopy(instructions), 12).run()
    )
