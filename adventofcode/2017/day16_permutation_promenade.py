"""
--- Day 16: Permutation Promenade ---
You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p.
They start by standing in a line:
a stands in position 0,
b stands in position 1,
and so on until p,
which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front,
but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
Exchange, written xA/B, makes the programs at positions A and B swap places.
Partner, written pA/B, makes the programs named A and B swap places.
For example, with only five programs standing in a line (abcde),
they could do the following dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.
After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input).
In what order are the programs standing after their dance?
"""

import unittest
from string import ascii_lowercase
from typing import Iterable


def spin(sent: str, i: int):
    return sent[-i:] + sent[:len(sent) - i]


def exchange(sent: str, i: int, j: int):
    ls = list(sent)
    reg = ls[i]
    ls[i] = ls[j]
    ls[j] = reg

    return ''.join(ls)


def partner(sent: str, a: str, b: str):
    i, j = sent.index(a), sent.index(b)
    return exchange(sent, i, j)


def parser(literals: Iterable[str]):
    mapping = dict(s=spin, x=exchange, p=partner)

    for li in literals:

        prefix = li[0]

        args = [int(x) if x.isdigit() else x for x in li[1:].split('/')]

        yield (mapping[prefix], args)


class Part01Test(unittest.TestCase):
    def test_spin(self):
        sent = 'abcde'
        expect = 'eabcd'

        self.assertEqual(spin(sent, 1), expect)

    def test_exchange(self):
        sent = 'abcde'
        expect = 'dbcae'

        self.assertEqual(exchange(sent, 0, 3), expect)

    def test_partner(self):
        sent = 'abcde'
        expect = 'dbcae'

        self.assertEqual(partner(sent, 'a', 'd'), expect)

    def test_parser(self):
        literals = ['s1', 'x3/4', 'pe/b']

        expect = [(spin, [1]), (exchange, [3, 4]), (partner, ['e', 'b'])]

        self.assertEqual(list(parser(literals)), expect)

    def test_example(self):
        sent = 'abcde'
        literals = ['s1', 'x3/4', 'pe/b']
        expect = 'baedc'

        for func, args in parser(literals):
            sent = func(sent, *args)

        self.assertEqual(sent, expect)


def part01(fpath: str):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        literals = f.read().strip().split(',')

    sent = ascii_lowercase[:16]

    for func, args in parser(literals):
        sent = func(sent, *args)

    print('- Part01 Answer:', sent)


"""
--- Part Two ---
Now that you're starting to get a feel for the dance moves,
you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance,
the programs perform it again and again: including the first dance,
a total of one billion (1,000,000,000) times.

In the example above, their second dance would begin with the order baedc,
and use the same dance moves:

s1, a spin of size 1: cbaed.
x3/4, swapping the last two programs: cbade.
pe/b, swapping programs e and b: ceadb.
In what order are the programs standing after their billion dances?
"""


def part02(fpath: str):

    with open(fpath, 'r') as f:
        literals = f.read().strip().split(',')

    original = ascii_lowercase[:16]
    results = [original]
    sent = original
    while True:
        for func, args in parser(literals):
            sent = func(sent, *args)
        if sent not in results:
            results.append(sent)
        else:
            break

    mod = (10**9) % len(results)

    print('Period:', len(results))
    print('- Part02 Answer:', results[mod])


if __name__ == '__main__':

    part01('day16_input.txt')  # fgmobeaijhdpkcln
    part02('day16_input.txt')  # lgmkacfjbopednhi
