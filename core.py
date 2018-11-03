from constants import FILE_PATH, FILE_EXTENSION, DIRECTORY_EXTENSION
import os

class Core:
    def __init__(self, input_file, core_num, cache):
        self.instructions = self.read_instructions(input_file, core_num)
        self.core_num = core_num
        self.cache = cache
        self.instruction_type = [0] * 4
        self.total_instructions = len(self.instructions)
        self.current_instruction = 0
        self.stall_cycle = 0

    def read_instructions(self, input_file, core_num):
        directory = ''.join([input_file, DIRECTORY_EXTENSION])
        filename = ''.join([input_file, '_', str(core_num), FILE_EXTENSION])
        path = os.path.join(FILE_PATH, directory, filename)

        instructions = []
        with open(path) as f:
            instructions = [tuple([int(i, 0) for i in line.split()]) for line in f]
        print(instructions)
        return instructions

    def execute_instruction(self):
        if self.current_instruction >= self.total_instructions:
            return None
        else:
            self.current_instruction += 1
            return self.instructions[self.current_instruction]

    def stall_instruction(self):
        self.current_instruction -= 1

    def is_busy(self):
        if self.stall_cycle <= 1:
            self.stall_cycle = 0
            return False
        else:
            self.stall_cycle -= 1
            return True

    def set_cycle_busy(self, cycles):
        self.stall_cycle += cycles
