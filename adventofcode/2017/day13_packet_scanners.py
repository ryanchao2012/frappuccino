"""
--- Day 13: Packet Scanners ---
You need to cross a vast firewall.
The firewall consists of several layers, each with a security scanner that moves back and forth across the layer.
To succeed, you must not be detected by a scanner.

By studying the firewall briefly,
you are able to record (in your puzzle input) the depth of each layer
and the range of the scanning area for the scanner within it, written as depth: range.
Each layer has a thickness of exactly 1. A layer at depth 0 begins immediately inside the firewall;
a layer at depth 1 would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4
This means that there is a layer immediately inside the firewall (with range 3),
a second layer immediately after that (with range 2), a third layer which begins at depth 4 (with range 4),
and a fourth layer which begins at depth 6 (also with range 4). Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]
Within each layer, a security scanner moves back and forth within its range.
Each security scanner starts at the top and moves down until it reaches the bottom,
then moves up until it reaches the top, and repeats.
A security scanner takes one picosecond to move one step.
Drawing scanners as S, the first few picoseconds look like this:


Picosecond 0:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]
Your plan is to hitch a ride on a packet about to move through the firewall.
The packet will travel along the top of each layer, and it moves at one layer per picosecond.
Each picosecond, the packet moves one layer forward (its first move takes it into layer 0),
and then the scanners move one step. If there is a scanner at the top of the layer as your packet enters it, you are caught.
(If a scanner moves into the top of its layer while you are there, you are not caught:
it doesn't have time to notice you before you leave.)
If you were to do this in the configuration above, marking your current position with parentheses,
your passage through the firewall would look like this:

Initial state:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 0:
 0   1   2   3   4   5   6
(S) [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 1:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] (S) ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] (.) ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 4:
 0   1   2   3   4   5   6
[S] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 5:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... ... [S] (.) [S]
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]


Picosecond 6:
 0   1   2   3   4   5   6
[ ] [S] ... ... [S] ... (S)
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]
In this situation, you are caught in layers 0 and 6,
because your packet entered the layer when its scanner was at the top when you entered it.
You are not caught in layer 1, since the scanner moved into the top of the layer once you were already there.

The severity of getting caught on a layer is equal to its depth multiplied by its range.
(Ignore layers in which you do not get caught.) The severity of the whole trip is the sum of these values.
In the example above, the trip severity is 0*3 + 6*4 = 24.

Given the details of the firewall you've recorded, if you leave immediately, what is the severity of your whole trip?
"""

import unittest
from typing import Callable, List, Tuple


def layer_parser(line: str) -> Tuple[int, int]:

    layer, depth = line.split(':')

    return int(layer.strip()), int(depth.strip())


def sum_severity(layers: List[Tuple[int, int]]):

    severity = 0

    for picosecond, depth in (layers):
        if depth == 0:
            continue

        if depth == 1 or picosecond % (2 * depth - 2) == 0:
            severity += (picosecond * depth)

    return severity


class Part01Test(unittest.TestCase):

    literals = ("""
        0: 3
        1: 2
        4: 4
        6: 4
        """)

    def test_parser(self):
        expect = [(0, 3), (1, 2), (4, 4), (6, 4)]

        layers = []

        for line in self.literals.strip().split('\n'):
            layers.append(layer_parser(line))

        self.assertEqual(layers, expect)

    def test_severity(self):
        layers = []
        for line in self.literals.strip().split('\n'):
            layers.append(layer_parser(line))

        expect = 24

        self.assertEqual(sum_severity(layers), expect)


def part01(fpath: str):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()

    print(runner.run(suite))

    with open(fpath, 'r') as f:
        layers = [layer_parser(line) for line in f.read().strip().split('\n')]

    print('- Part01 Answer:', sum_severity(layers))


"""
--- Part Two ---
Now, you need to pass through the firewall without being caught - easier said than done.

You can't control the speed of the packet, but you can delay it any number of picoseconds.
For each picosecond you delay the packet before beginning your trip, all security scanners move one step.
You're not in the firewall during this time; you don't enter layer 0 until you stop delaying the packet.

In the example above, if you delay 10 picoseconds (picoseconds 0 - 9), you won't get caught:

State after delaying:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 10:
 0   1   2   3   4   5   6
( ) [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 11:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[S] (S) ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 12:
 0   1   2   3   4   5   6
[S] [S] (.) ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 13:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 14:
 0   1   2   3   4   5   6
[ ] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 15:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... ... [ ] (.) [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 16:
 0   1   2   3   4   5   6
[S] [S] ... ... [ ] ... ( )
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]
Because all smaller delays would get you caught,
the fewest number of picoseconds you would need to delay to get through safely is 10.

What is the fewest number of picoseconds that you need to delay the packet to pass through the firewall without being caught?
"""


def get_caught_sequence_args(layer: int, depth: int) -> Tuple[int, int]:
    """Get the caught sequence according the given `layer` and `depth`.

    The caught points from a given layer form a `arithmetic sequence`(https://en.wikipedia.org/wiki/Arithmetic_progression),
    general form: An = A0 + n * d
    in which, the common difference, d, is the period of the harmonic motion of the scanner,
    i.e., period = d = depth * 2 - 2, and
    the first term, A0, is larger than 0.

    Return A0 and d.
    """

    d = depth * 2 - 2  # depth must larger than 1
    first = (1 + (layer // d)) * d - layer

    return d, first


def get_arith_seq(difference: int, first_term: int):
    def inner(idx: int):
        return first_term + idx * difference

    return inner


def find_min_escape_delay(layers: Tuple[int, int], max_iteration=10):
    """Find the minimum delay to escape.

    Get caught sequence of each layer,
    then iterate the process:
    1. get the n-th term from all sequences,
    2. sort them, return the first non-successive number.
    """

    arith_sequences = []
    curr_max = 0

    for layer, depth in layers:
        d, first = get_caught_sequence_args(layer, depth)
        func = get_arith_seq(d, first)  # noqa
        curr = func(0)
        if curr > curr_max:
            curr_max = curr
        arith_sequences.append(dict(seq=func, idx=1, current=curr))

    idx = 0
    next_max = curr_max
    while max_iteration > idx:
        #  print('----')
        terms = []
        for arith in arith_sequences:
            while arith['current'] <= curr_max:
                terms.append(arith['current'])
                arith['current'] = arith['seq'](arith['idx'])
                arith['idx'] += 1

                if arith['current'] > next_max:
                    next_max = arith['current']

        sorted_terms = sorted(set(terms))

        # print(f'sorted_terms: {sorted_terms}')
        for i, j in zip(sorted_terms[:-1], sorted_terms[1:]):
            if j - i > 1:
                return i + 1

        # print(f'curr_max: {curr_max}')
        curr_max = next_max
        idx += 1

    raise AssertionError()


class Part02Test(unittest.TestCase):

    literals = ("""
        0: 3
        1: 2
        4: 4
        6: 4
        """)

    def test_arith_seq(self):
        expect = [(4, 4), (2, 1), (6, 2), (6, 6)]

        ariths = []
        for line in self.literals.strip().split('\n'):
            ariths.append(get_caught_sequence_args(*layer_parser(line)))

        self.assertEqual(ariths, expect)

    def test_escape(self):
        layers = []
        for line in self.literals.strip().split('\n'):
            layers.append(layer_parser(line))

        expect = 10

        self.assertEqual(find_min_escape_delay(layers), expect)


def part02(fpath: str):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part02Test))
    runner = unittest.TextTestRunner()

    print(runner.run(suite))

    with open(fpath, 'r') as f:
        layers = [layer_parser(line) for line in f.read().strip().split('\n')]

    print('- Part02 Answer:', find_min_escape_delay(layers, 1000000))


if __name__ == '__main__':

    part01('day13_input.txt')  # 1300
    part02('day13_input.txt')  # 3870382
