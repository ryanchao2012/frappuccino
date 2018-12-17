"""
--- Day 14: Disk Defragmentation ---
Suddenly, a scheduled job activates the system's disk defragmenter.
Were the situation different, you might sit and watch it for a while,
but today, you just don't have that kind of time.
It's soaking up valuable system resources that are needed elsewhere,
and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid;
each square of the grid is either free or used.
On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid;
each hash contains 128 bits which correspond to individual grid squares.
Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row.
For example, if your key string were flqrgnkx,
then the first row would be given by the bits of the knot hash of flqrgnkx-0,
the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits;
each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits.
To convert to bits, turn each hexadecimal digit to its equivalent binary value,
high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111,
and so on; a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows,
using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V
In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?
"""

import unittest
from itertools import product
from typing import List, Set, Tuple

from functional import seq

import day10_knot_hash as knot_hash


def fill_squares(inputs: str, dimension: int = 8, **kh_kwargs):
    return list(seq(range(dimension))
                .map(lambda i: f'{inputs}-{i}')
                .map(lambda e: knot_hash.encode(e, **kh_kwargs))
                .map(lambda e: ''.join(['0' * any([x == '0', x == '1']) +
                                        bin(int(x, base=16))[-4:].replace('b', '0')
                                        for x in e])))  # yapf: disable


def sum_squares(squares: List[str]):
    def sum_binaries(binaries: str):
        return (seq(iter(binaries))
                .filter(lambda e: e == '1')
                .len())  # yapf: disable

    return (seq(squares)
            .map(sum_binaries)
            .reduce(lambda x, y: x + y))  # yapf: disable


class Part01Test(unittest.TestCase):

    inputs = 'flqrgnkx'

    def test_squares(self):
        expect = [
            '11010100',
            '01010101',
            '00001010',
            '10101101',
            '01101000',
            '11001001',
            '01000100',
            '11010110'
        ]  # yapf: disable

        self.assertEqual(
            [s[:8] for s in fill_squares(self.inputs, dimension=8)], expect)

    def test_sum_squares(self):
        expect = 8108

        self.assertEqual(
            sum_squares(fill_squares(self.inputs, dimension=128)), expect)


def part01(inputs: str = ''):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    print('- Part01 Answer:', sum_squares(fill_squares(inputs, dimension=128)))


"""
--- Part Two ---
Now, all the defragmenter needs to know is the number of regions.
A region is a group of used squares that are all adjacent, not including diagonals.
Every used square is in exactly one region:
lone used squares form their own isolated regions,
while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible,
each marked with a distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V
Of particular interest is the region marked 8;
while it does not appear contiguous in this small view,
all of the squares marked 8 are connected when considering the whole 128x128 grid.
In total, in this example, 1242 regions are present.

How many regions are present given your key string?
"""


def find_regions(inputs: str, dimension: int = 8, **kh_kwargs):

    squares = fill_squares(inputs, dimension=dimension)

    # for s in squares[:dimension]:
    #     print(s[:dimension])

    # return
    all_coords = list(product(range(dimension), repeat=2))
    mapping = {}

    def get_neighbors(coord: Tuple[int, int], group: Set) -> None:
        i, j = coord
        others = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

        for that in others:
            x, y = that
            if all([x >= 0, y >= 0, x < dimension, y < dimension]):
                if squares[x][y] == '1' and (that not in group):
                    group.add(that)
                    get_neighbors(that, group)

    grp_index = 0
    regions = {}
    while len(all_coords) > 0:

        this = all_coords.pop()
        i, j = this
        if squares[i][j] == '1':
            group = set([this])
            get_neighbors(this, group)
            regions[grp_index] = group
            for each in group:
                mapping[each] = grp_index
                if each != this:
                    all_coords.remove(each)

            grp_index += 1

    # regions = {}

    return mapping, regions


class Part02Test(unittest.TestCase):
    def test_find_regions(self):
        expect = 1242

        mapping, regions = find_regions('flqrgnkx', dimension=128)
        self.assertEqual(len(set(mapping.values())), len(regions))
        self.assertEqual(len(regions), expect)


def part02(inputs: str = ''):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part02Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    mapping, regions = find_regions(inputs, dimension=128)
    print('- Part02 Answer:', len(regions))


if __name__ == '__main__':

    # part01('nbysizxe')  # 8216
    part02('nbysizxe')
