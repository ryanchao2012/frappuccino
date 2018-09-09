"""
--- Day 5: A Maze of Twisty Trampolines, All Alike ---
An urgent interrupt arrives from the CPU:
it's trapped in a maze of jump instructions,
and it would like assistance from any programs with spare cycles to help find the exit.

The message includes a list of the offsets for each jump.
Jumps are relative: -1 moves to the previous instruction, and 2 skips the next one.
Start at the first instruction in the list. The goal is to follow the jumps until one leads outside the list.

In addition, these instructions are a little strange; after each jump,
the offset of that instruction increases by 1.
So, if you come across an offset of 3, you would move three instructions forward,
but change it to a 4 for the next time it is encountered.

For example, consider the following list of jump offsets:

0
3
0
1
-3
Positive jumps ("forward") move downward; negative jumps move upward.
For legibility in this example, these offset values will be written all on one line,
with the current instruction marked in parentheses. The following steps would be taken before an exit is found:

(0) 3  0  1  -3  - before we have taken any steps.
(1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all). Fortunately, the instruction is then incremented to 1.
 2 (3) 0  1  -3  - step forward because of the instruction we just modified. The first instruction is incremented again, now to 2.
 2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
 2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
 2  5  0  1  -2  - jump 4 steps forward, escaping the maze.
In this example, the exit is reached in 5 steps.

How many steps does it take to reach the exit?
"""

import unittest
from typing import List


def check_instruction_valid(ls: List[int]) -> bool:
    return all((i + x) >= 0 for i, x in enumerate(ls))


def find_instruction_steps(ls: List[int]) -> int:
    length = len(ls)
    ls_ = ls.copy()
    index = 0
    steps = 0
    while index < length:
        instuction = ls_[index]
        ls_[index] += 1
        index += instuction
        steps += 1

    return steps, ls_


class Part01Test(unittest.TestCase):

    def test_checker(self):
        self.assertTrue(check_instruction_valid([0, 0, -1, -2, 2, -5]))
        self.assertFalse(check_instruction_valid([0, -2, 1, 2, 0, -4]))

    def test_steps(self):
        ls = [0, 3, 0, 1, -3]
        steps, new_ls = find_instruction_steps(ls)

        self.assertEqual(new_ls, [2, 5, 0, 1, -2])
        self.assertEqual(steps, 5)


def part01(fpath):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        ls = [int(line) for line in f]

    if not check_instruction_valid(ls):
        raise ValueError

    steps, _ = find_instruction_steps(ls)
    print('- Part01 Answer:', steps)


"""
--- Part Two ---
Now, the jumps are even stranger: after each jump,
if the offset was three or more, instead decrease it by 1. Otherwise, increase it by 1 as before.

Using this rule with the above example, the process now takes 10 steps,
and the offset values after finding the exit are left as 2 3 2 3 -1.

How many steps does it now take to reach the exit?
"""


def find_instruction_strange_steps(ls: List[int]) -> int:
    length = len(ls)
    ls_ = ls.copy()
    index = 0
    steps = 0
    while index < length:
        offset = ls_[index]
        if offset >= 3:
            ls_[index] += (-1)
        else:
            ls_[index] += 1
        index += offset
        steps += 1

    return steps, ls_


class Part02Test(unittest.TestCase):

    def test_steps(self):
        ls = [0, 3, 0, 1, -3]
        steps, new_ls = find_instruction_strange_steps(ls)

        self.assertEqual(new_ls, [2, 3, 2, 3, -1])
        self.assertEqual(steps, 10)


def part02(fpath):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part02Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        ls = [int(line) for line in f]

    if not check_instruction_valid(ls):
        raise ValueError

    steps, _ = find_instruction_strange_steps(ls)
    print('- Part02 Answer:', steps)

if __name__ == '__main__':

    part01('./day05_part01_input.txt')  # 364539
    part02('./day05_part01_input.txt')  # 27477714
