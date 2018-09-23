"""
--- Day 8: I Heard You Like Registers ---
You receive a signal directly from the CPU.
Because of your recent assistance with jump instructions,
it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify,
whether to increase or decrease that register's value,
the amount by which to increase or decrease it, and a condition.
If the condition fails, skip the instruction without modifying the register.
The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
These instructions would be processed as follows:

Because a starts at 0, it is not greater than 1, and so b is not modified.
a is increased by 1 (to 1) because b is less than 5 (it is 0).
c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
c is increased by -20 (to -10) because c is equal to 10.
After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to).
However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?
"""
import operator as op
import unittest
from typing import Callable, Dict

import attr


@attr.s(auto_attribs=True)
class Instruction:
    target: str
    operator: Callable[[int, int], int]
    value: int
    reference: str
    condition: Callable[[int, int], bool]
    weight: int


operators = {'inc': op.add,
             'dec': op.sub,
             '>': op.gt,
             '>=': op.ge,
             '<': op.lt,
             '<=': op.le,
             '==': op.eq,
             '!=': op.ne}


def parsing_instruction(literal: str) -> Instruction:
    reg1, op, val1, _, reg2, cond, val2 = literal.split()

    return Instruction(target=reg1,
                       operator=operators[op],
                       value=int(val1),
                       reference=reg2,
                       condition=operators[cond],
                       weight=int(val2))


class Part01Test(unittest.TestCase):

    def test_parser(self):
        inputs = """
        b inc 5 if a > 1
        a inc 1 if b < 5
        c dec -10 if a >= 1
        c inc -20 if c == 10
        """

        expections = [
            Instruction('b', op.add, 5, 'a', op.gt, 1),
            Instruction('a', op.add, 1, 'b', op.lt, 5),
            Instruction('c', op.sub, -10, 'a', op.ge, 1),
            Instruction('c', op.add, -20, 'c', op.eq, 10)
        ]

        for line, exp in zip(inputs.strip().split('\n'), expections):
            self.assertEqual(parsing_instruction(line.strip()), exp)


def part01(path: str):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    registers = {}

    with open(path, 'r') as f:
        for line in f:
            ins = parsing_instruction(line.strip())
            if ins.target not in registers:
                registers[ins.target] = 0
            if ins.reference not in registers:
                registers[ins.reference] = 0

            if ins.condition(registers[ins.reference], ins.weight):
                registers[ins.target] = ins.operator(
                    registers[ins.target], ins.value)

    print('- Part01 Answer:', max(registers.values()))


"""
--- Part Two ---
To be safe, the CPU also needs to know the highest value held in any register
during this process so that it can decide how much memory to allocate to these operations.
For example, in the above instructions,
the highest value ever held was 10 (in register c after the third instruction was evaluated).
"""


def part02(path: str):

    registers: Dict[str, int] = {}
    highest: int = 0

    with open(path, 'r') as f:
        for line in f:
            ins = parsing_instruction(line.strip())
            if ins.target not in registers:
                registers[ins.target] = 0
            if ins.reference not in registers:
                registers[ins.reference] = 0

            if ins.condition(registers[ins.reference], ins.weight):
                registers[ins.target] = ins.operator(
                    registers[ins.target], ins.value)

            m = max(registers.values())
            if m > highest:
                highest = m

    print('- Part02 Answer:', highest)


if __name__ == '__main__':
    part01('day08_input.txt')  # 5075
    part02('day08_input.txt')  # 7310
