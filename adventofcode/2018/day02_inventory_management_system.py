"""
--- Day 2: Inventory Management System ---
You stop falling through time, catch your breath, and check the screen on the device.
"Destination reached. Current Year: 1518. Current Location: North Pole Utility Closet 83N10."
You made it! Now, to find those anomalies.

Outside the utility closet, you hear footsteps and a voice. "...I'm not sure either.
But now that so many people have chimneys, maybe he could sneak in that way?"
Another voice responds, "Actually, we've been working on a new kind of suit
that would let him fit through tight spaces like that.
But, I heard that a few days ago, they lost the prototype fabric,
the design plans, everything! Nobody on the team can even seem to remember
important details of the project!"

"Wouldn't they have had enough fabric to fill several boxes in the warehouse?
They'd be stored together, so the box IDs should be similar.
Too bad it would take forever to search the warehouse for two similar box IDs..."
They walk too far away to hear any more.

Late at night, you sneak to the warehouse - who knows what kinds of paradoxes
you could cause if you were discovered - and use your fancy wrist device to quickly scan
every box and produce a list of the likely candidates (your puzzle input).

To make sure you didn't miss any, you scan the likely candidate boxes again,
counting the number that have an ID containing exactly two of any letter
and then separately counting those with exactly three of any letter.
You can multiply those two counts together to get a rudimentary checksum
and compare it to what your device predicts.

For example, if you see the following box IDs:

abcdef contains no letters that appear exactly two or three times.
bababc contains two a and three b, so it counts for both.
abbcde contains two b, but no letter appears exactly three times.
abcccd contains three c, but no letter appears exactly two times.
aabcdd contains two a and two d, but it only counts once.
abcdee contains two e.
ababab contains three a and three b, but it only counts once.
Of these box IDs, four of them contain a letter which appears exactly twice,
and three of them contain a letter which appears exactly three times.
Multiplying these together produces a checksum of 4 * 3 = 12.

What is the checksum for your list of box IDs?
"""

import operator
from unittest import TestCase as TC
from misc import run_testsuite
from typing import *  # noqa
from collections import Counter
from itertools import combinations
from functools import reduce


class Part01Test(TC):
    @property
    def box_ids(self):

        return (ids for ids in [
            'abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee',
            'ababab'
        ])

    def test_checksum(self):

        self.assertEqual(calc_checksum(self.box_ids), 12)

    def test_contain_two_or_three(self):
        expects = [(0, 0), (1, 1), (1, 0), (0, 1), (1, 0), (1, 0), (0, 1)]

        for sent, expect in zip(self.box_ids, expects):
            self.assertEqual(contain_two_or_three(sent), expect)


def contain_two_or_three(sent: str) -> Tuple[int, int]:
    counts = Counter(sent).values()

    return (int(2 in counts), int(3 in counts))


def calc_checksum(it: Iterable[str]) -> int:

    return operator.mul(*reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]),
                                (contain_two_or_three(e) for e in it), (0, 0)))


def part01(path: str):

    run_testsuite(Part01Test)

    with open(path, 'r') as f:
        checksum = calc_checksum(f)

    print('- Part01 Answer:', checksum)


"""
--- Part Two ---
Confident that your list of box IDs is complete,
you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings.
For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth).
However, the IDs fghij and fguij differ by exactly one character, the third (h and u).
Those must be the correct boxes.

What letters are common between the two correct box IDs?
(In the example above,
this is found by removing the differing character from either ID, producing fgij.)
"""


def sum_differences(sent1: str, sent2: str) -> int:
    len1, len2 = len(sent1), len(sent2)
    sent_long, sent_short = (sent1, sent2) if len1 >= len2 else (sent2, sent1)
    sent_short_padded = sent_short + (' ' * abs(len1 - len2))

    return sum((w1 != w2) for w1, w2 in zip(sent_long, sent_short_padded))


def find_correct_pair(
        it: Iterable[Tuple[str, str]]) -> Optional[Tuple[str, str]]:

    for sent1, sent2 in it:
        if sum_differences(sent1, sent2) == 1:
            return (sent1, sent2)


class Part02Test(TC):
    @property
    def box_ids(self):
        return """abcde
                  fghij
                  klmno
                  pqrst
                  fguij
                  axcye
                  wvxyz""".split()

    @property
    def box_pairs(self):
        return [
            ('abcde', 'abcde'),
            ('abcde', 'fghij'),
            ('abcde', 'axcye'),
            ('fghij', 'fguij'),
        ]

    def test_sum_differences(self):
        expects = [0, 5, 2, 1]

        for (sent1, sent2), expect in zip(self.box_pairs, expects):
            self.assertEqual(sum_differences(sent1, sent2), expect)

    def test_find_correct_pair(self):
        self.assertEqual(
            set(find_correct_pair(combinations(self.box_ids, 2))),
            set(['fghij', 'fguij']))

    def test_get_commons(self):
        self.assertEqual(get_commons('fghij', 'fguij'), 'fgij')


def get_commons(sent1: str, sent2: str) -> str:
    len1, len2 = len(sent1), len(sent2)
    sent_long, sent_short = (sent1, sent2) if len1 >= len2 else (sent2, sent1)
    sent_short_padded = sent_short + (' ' * abs(len1 - len2))
    commons = [w1 for w1, w2 in zip(sent_long, sent_short_padded) if w1 == w2]
    return ''.join(commons)


def part02(path: str):

    run_testsuite(Part02Test)

    with open(path, 'r') as f:
        commons = get_commons(*find_correct_pair(combinations(f, 2)))

    print('- Part02 Answer:', commons)


if __name__ == "__main__":
    part01('day02_input.txt')  # 7350
    part02('day02_input.txt')  # wmlnjevbfodamyiqpucrhsukg