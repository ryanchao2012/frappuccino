"""
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab.
The Elves are making decent progress,
but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually,
you can do better. You scan the chemical composition of the suit's material
and discover that it is formed by extremely long polymers
(one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other
such that two adjacent units of the same type and opposite polarity are destroyed.
Units' types are represented by letters; units' polarity is represented by capitalization.
For instance, r and R are units with the same type but opposite polarity,
whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned?
(Note: in this puzzle and others, the input is large;
if you copy/paste your input, make sure you get the whole thing.)
"""

from typing import *  # noqa
from unittest import TestCase as TC
from misc import run_testsuite


class Node:
    def __init__(self, name: str, value: str, link=None):
        self.name = name
        self.value = value
        self.link = link

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'<Node: ({self.name}, {self.value})>'


def gen_linked_list(letters: str) -> Iterable[Node]:
    node = Node(0, letters[0])
    for i, ch in enumerate(letters[1:], 1):
        link = Node(i, ch)
        node.link = link
        yield node
        node = link
    yield node


def fulling_reaction(nodes: Iterable[Node]) -> List[Node]:

    remaining = []

    for node in nodes:
        if len(remaining) == 0:
            remaining.append(node)
        else:
            tail = remaining[-1]
            if abs(ord(tail.value) - ord(node.value)) == 32:
                remaining.pop()
            else:
                tail.link = node
                remaining.append(node)

    return remaining


class Part01Test(TC):
    @property
    def letters(self):
        return 'dabAcCaCBAcCcaDA'

    def test_gen_linked_list(self):

        prev_link: Node = None
        for i, (node, ch) in enumerate(
                zip(gen_linked_list(self.letters), self.letters)):

            self.assertEqual((node.name, node.value), (i, ch))
            if prev_link is not None:
                self.assertEqual((prev_link.name, prev_link.value),
                                 (node.name, node.value))
            prev_link = node.link

        self.assertIsNone(prev_link)

    def test_fulling_reaction(self):

        remaining = fulling_reaction(gen_linked_list(self.letters))
        units = ''.join(r.value for r in remaining)

        self.assertEqual(len(remaining), 10)
        self.assertEqual(units, 'dabCBAcaDA')


def part01(path: str):

    run_testsuite(Part01Test)

    with open(path, 'r') as f:
        letters = f.read().strip()

    remaining = fulling_reaction(gen_linked_list(letters))

    print('- Part01 Answer:', len(remaining))


"""
--- Part Two ---
Time to improve the polymer.

One of the unit types is causing problems;
it's preventing the polymer from collapsing as much as it should.
Your goal is to figure out which unit type is causing the most problems,
remove all instances of it (regardless of polarity), fully react the remaining polymer,
and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD.
Fully reacting this polymer produces dbCBcD, which has length 6.
Removing all B/b units produces daAcCaCAcCcaDA.
Fully reacting this polymer produces daCAcaDA, which has length 8.
Removing all C/c units produces dabAaBAaDA.
Fully reacting this polymer produces daDA, which has length 4.
Removing all D/d units produces abAcCaCBAcCcaA.
Fully reacting this polymer produces abCBAc, which has length 6.
In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce
by removing all units of exactly one type and fully reacting the result?
"""

from string import ascii_lowercase, ascii_uppercase
import re


def find_shortest_polymer(original: str) -> int:
    shortest_length = len(original)

    for lo, up in zip(ascii_lowercase, ascii_uppercase):
        letters = re.sub(f'[{lo}{up}]', r'', original)
        remaining = fulling_reaction(gen_linked_list(letters))
        length = len(remaining)
        if length < shortest_length:
            shortest_length = length

    return shortest_length


class Part02Test(TC):
    @property
    def letters(self):
        return 'dabAcCaCBAcCcaDA'

    def test_find_shortest(self):
        self.assertEqual(find_shortest_polymer(self.letters), 4)


def part02(path: str):

    run_testsuite(Part02Test)

    with open(path, 'r') as f:
        letters = f.read().strip()

    shortest_length = find_shortest_polymer(letters)

    print('- Part02 Answer:', shortest_length)


if __name__ == "__main__":
    part01('day05_input.txt')  # 11540
    part02('day05_input.txt')  # 6918