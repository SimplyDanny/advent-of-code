from common import print_results, readlines


class Instruction:
    def __init__(self, command, arg1, arg2=''):
        self.command = command
        self.arg1 = arg1
        self.arg2 = arg2

class Program:
    def __init__(self, instructions, register_c_start=0):
        self.instructions = instructions
        self.number_instructions = len(self.instructions)
        self.position = 0
        self.reg = {'a': 0, 'b': 0, 'c': register_c_start, 'd': 0}
        self.commands = {
            'cpy': self.command_cpy,
            'inc': self.command_inc,
            'dec': self.command_dec,
            'jnz': self.command_jnz
        }

    def run(self):
        while True:
            inst = self.instructions[self.position]
            self.commands[inst.command](inst.arg1, inst.arg2)
            if self.position >= self.number_instructions or self.position < 0:
                break
        return self.reg['a']

    def command_cpy(self, arg1, arg2):
        self.reg[arg2] = self.get_value(arg1)
        self.position += 1

    def command_inc(self, arg1, arg2):
        self.reg[arg1] += 1
        self.position += 1

    def command_dec(self, arg1, arg2):
        self.reg[arg1] -= 1
        self.position += 1

    def command_jnz(self, arg1, arg2):
        self.position += self.get_value(arg2) if self.is_not_zero(arg1) else 1

    def is_not_zero(self, arg):
        return self.get_value(arg) != 0

    def get_value(self, arg):
        return int(arg) if arg.lstrip('-').isdigit() else self.reg[arg]


if __name__ == '__main__':
    instructions = [Instruction(*line.split()) for line in readlines(__file__)]

    print_results(
        Program(instructions, 0).run(),
        Program(instructions, 1).run()
    )
