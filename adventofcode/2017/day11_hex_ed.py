"""
--- Day 11: Hex Ed ---
Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you,
clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north,
northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
You have the path the child process took. Starting where he started,
you need to determine the fewest number of steps required to reach him.
(A "step" means to move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).y
"""

import unittest
from collections import Counter
from typing import Dict


def reducing(src: Dict[str, int]) -> Dict[str, int]:
    """Reduce hex steps to `n`, `ne` and `nw`."""
    dest: Dict[str, int] = dict(n=src['n'] - src['s'],
                                ne=src['ne'] - src['sw'],
                                nw=src['nw'] - src['se'])

    return rotating(dest)


def rotating(src: Dict[str, int]) -> Dict[str, int]:
    """Let `n` always be positive and abs(n) always be the largest."""

    counts = sorted([(k, abs(v)) for k, v in src.items()], key=lambda e: e[1], reverse=True)

    new_n = counts[0][0]
    dest = dict(n=src[new_n])

    if new_n == 'ne':
        dest['nw'] = src['n']
        dest['ne'] = -src['nw']

    elif new_n == 'nw':
        dest['ne'] = src['n']
        dest['nw'] = -src['ne']
    else:
        dest['ne'] = src['ne']
        dest['nw'] = src['nw']

    if dest['n'] < 0:
        dest['n'] *= -1
        dest['ne'] *= -1
        dest['nw'] *= -1

    return dest


def canceling(src: Dict[str, int]) -> Dict[str, int]:

    dest = dict(**src)

    bigger, smaller = ('ne', 'nw') if dest['ne'] >= dest['nw'] else ('nw', 'ne')
    c = abs(dest[smaller])
    if dest[smaller] < 0:
        dest['n'] -= c
        dest[bigger] += c
    else:
        dest['n'] += c
        dest[bigger] -= c
    dest[smaller] = 0

    return dest


def shortest_steps(hex_counts: Dict[str, int]) -> int:

    return sum(v for _, v in canceling(reducing(hex_counts)).items())


class Part01Test(unittest.TestCase):

    def test_shortest_steps(self):
        """
        ne,ne,ne is 3 steps away.
        ne,ne,sw,sw is 0 steps away (back where you started).
        ne,ne,s,s is 2 steps away (se,se).
        se,sw,se,sw,sw is 3 steps away (s,s,sw).
        """

        inputs = ['ne,ne,ne', 'ne,ne,sw,sw', 'ne,ne,s,s', 'se,sw,se,sw,sw']
        expects = [3, 0, 2, 3]

        for literal, exp in zip(inputs, expects):
            self.assertEqual(shortest_steps(Counter(literal.strip().split(','))), exp)


def part01(fpath: str):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        steps = Counter(f.read().strip().split(','))

    print('- Part01 Answer:', shortest_steps(steps))


"""
--- Part Two ---
How many steps away is the furthest he ever got from his starting position?
"""


def part02(fpath: str):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        steps = f.read().strip().split(',')

    m = 0
    for i in range(len(steps)):
        s = shortest_steps(Counter(steps[:i + 1]))
        if s > m:
            m = s

    print('- Part02 Answer:', m)


if __name__ == '__main__':

    part01('day11_input.txt')  # 743
    part02('day11_input.txt')  # 1493
