"""
--- Day 3: No Matter How You Slice It ---
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit
(thanks to someone who helpfully wrote its box IDs on the wall of the warehouse
in the middle of the night).
Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit.
All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric.
Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge,
2 inches from the top edge, 5 inches wide, and 4 inches tall.
Visually, it claims the square inches of fabric represented by #
(and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap,
causing two or more claims to cover part of the same areas.
For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2.
(Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric.
How many square inches of fabric are within two or more claims?
"""

import numpy as np
from unittest import TestCase as TC
from misc import run_testsuite
from typing import *  # noqa
from attr import attrs


@attrs(slots=True, auto_attribs=True)
class Claim:
    claim_id: int
    col: int
    row: int
    width: int
    height: int


def literal_parser(lit: str) -> Claim:
    lit_id, _, lit_coord, lit_area = lit.split(' ')
    col, row = [int(e) for e in lit_coord[:-1].split(',')]
    width, height = [int(e) for e in lit_area.split('x')]
    claim_id = int(lit_id[1:])

    return Claim(
        claim_id=claim_id, height=height, width=width, row=row, col=col)


def sum_overlap_squares(claims: Iterable[Claim], sidelen: int = 1000) -> int:
    fabric = np.zeros((sidelen, sidelen))

    for claim in claims:
        fabric[claim.row:claim.row + claim.height, claim.col:claim.col +
               claim.width] += 1.0

    return int((fabric > 1).sum())


class Part01Test(TC):
    @property
    def lit_claims(self):
        return ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']

    def test_literal_parser(self):
        expects = [
            Claim(claim_id=1, height=4, width=4, row=3, col=1),
            Claim(claim_id=2, height=4, width=4, row=1, col=3),
            Claim(claim_id=3, height=2, width=2, row=5, col=5)
        ]

        for lit, expect in zip(self.lit_claims, expects):
            self.assertEqual(literal_parser(lit), expect)

    def test_sum_overlap_squares(self):
        self.assertEqual(
            sum_overlap_squares(
                [literal_parser(lit) for lit in self.lit_claims]), 4)


def part01(path: str):

    run_testsuite(Part01Test)

    with open(path, 'r') as f:
        overlap_squares = sum_overlap_squares(literal_parser(lit) for lit in f)

    print('- Part01 Answer:', overlap_squares)


"""
--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap
by even a single square inch of fabric with any other claim.
If you can somehow draw attention to it,
maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""


def find_intact_claim(claims: Iterable[Claim],
                      sidelen: int = 1000) -> Optional[Claim]:
    fabric = np.zeros((sidelen, sidelen))
    cached = []
    for claim in claims:
        fabric[claim.row:claim.row + claim.height, claim.col:claim.col +
               claim.width] += 1.0
        cached.append(claim)

    for claim in cached:
        if fabric[claim.row:claim.row + claim.height, claim.col:claim.col +
                  claim.width].sum() == claim.height * claim.width:
            return claim


class Part02Test(TC):
    @property
    def lit_claims(self):
        return ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']

    def test_find_intact_claim(self):
        self.assertEqual(
            find_intact_claim(
                literal_parser(lit) for lit in self.lit_claims).claim_id, 3)


def part02(path: str):

    run_testsuite(Part02Test)
    with open(path, 'r') as f:
        claim = find_intact_claim(literal_parser(lit) for lit in f)

    print('- Part02 Answer:', claim.claim_id)


if __name__ == "__main__":
    part01('day03_input.txt')  # 118840
    part02('day03_input.txt')  # 919