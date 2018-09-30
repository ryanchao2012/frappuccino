"""
--- Day 12: Digital Plumber ---
Walking along the memory banks of the stream,
you find a small village that is experiencing a little confusion:
some programs can't communicate with each other.

Programs in this village communicate using a fixed system of pipes.
Messages are passed between programs using these pipes,
but most programs aren't connected to each other directly. Instead,
programs pass messages between each other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their intended recipient,
and the programs suspect that some pipes are missing. They would like you to investigate.

You walk through the village and record the ID of each program
and the IDs with which it can communicate directly (your puzzle input).
Each program has one or more programs with which it can communicate,
and these pipes are bidirectional;
if 8 says it can communicate with 11, then 11 will say it can communicate with 8.

You need to figure out how many programs are in the group that contains program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record the following list:

    0 <-> 2
    1 <-> 1
    2 <-> 0, 3, 4
    3 <-> 2, 4
    4 <-> 2, 3, 6
    5 <-> 6
    6 <-> 4, 5
    In this example, the following programs are in the group that contains program ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.
    Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.

    How many programs are in the group that contains program ID 0?
"""

import unittest
from typing import Dict, List, Optional, Set


class Node:

    __slots__ = ('name', 'value', 'neighbors')

    def __init__(self, name: str, value: int = 0, neighbors: Optional[List['Node']] = None):
        self.name = name
        self.value = value
        self.neighbors = set()

        self.add_neighbors(neighbors or [])

    def add_neighbors(self, neighbors: Optional[List['Node']] = None):

        if neighbors is None:
            return

        for nb in neighbors:
            self._add_neighbor(nb)

    def __str__(self):

        return f'{self.name} -> {[nb.name for nb in self.neighbors]}'

    def __repr__(self):
        return str(self)

    def _add_neighbor(self, neighbor: 'Node', debug=False):

        if not isinstance(neighbor, self.__class__):
            return

        self.neighbors.add(neighbor)

        if debug:
            head = f'Node[{self.name}]'
            print(f'{head}: adding new neighbor `{neighbor.name}`')
            print(f'{" " * len(head)}: total neighbors: {self.neighbors}')


class Tree:

    __slots__ = ('_nodes',)

    def __init__(self):

        self._nodes = {}

    @property
    def nodes(self) -> Dict[str, Node]:
        return self._nodes

    def get_node(self, name: str) -> Optional[Node]:
        return self.nodes.get(name, None)

    def add_node(self, node: Node):

        for nb in node.neighbors:
            if nb.name not in self.nodes:
                self._nodes[nb.name] = nb  # XXX

        if node.name not in self.nodes:
            self._nodes[node.name] = node
        else:
            this = self.get_node(node.name)
            this.add_neighbors(node.neighbors)

    @classmethod
    def from_multilines(cls, lines: str):
        tree = cls()

        for line in lines.strip().split('\n'):

            name, nbs = node_parser(line)
            neighbors = [tree.get_node(nb) if nb in tree.nodes else Node(nb) for nb in nbs]
            tree.add_node(Node(name, neighbors=neighbors))

        return tree

    def get_group(self, node: Node, group: Set[Node]) -> None:
        group.add(node)

        for nb in node.neighbors:
            if nb not in group:
                self.get_group(nb, group)


def node_parser(literal: str):
    nm, nbs = literal.strip().split('<->')
    name = nm.strip()
    neighbors = [nb.strip() for nb in nbs.split(',')]
    return name, neighbors


class Part01Test(unittest.TestCase):

    literals = (
        """
        0 <-> 2
        1 <-> 1
        2 <-> 0, 3, 4
        3 <-> 2, 4
        4 <-> 2, 3, 6
        5 <-> 6
        6 <-> 4, 5
        """
    )

    def test_parser(self):
        expects = [
            ('0', ['2']),
            ('1', ['1']),
            ('2', ['0', '3', '4']),
            ('3', ['2', '4']),
            ('4', ['2', '3', '6']),
            ('5', ['6']),
            ('6', ['4', '5'])
        ]

        for li, exp in zip(self.literals.strip().split('\n'), expects):
            self.assertEqual(node_parser(li), exp)

    def test_neighbors(self):
        tree = Tree.from_multilines(self.literals)
        group = set()
        tree.get_group(tree.get_node('0'), group)
        self.assertEqual(len(group), 6)


def part01(fpath):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        tree = Tree.from_multilines(f.read())

    group = set()
    tree.get_group(tree.get_node('0'), group)
    print('- Part01 Answer:', len(group))


"""
--- Part Two ---
There are more programs than just the ones in the group containing program ID 0.
The rest of them have no way of reaching that group, and still might have no way of reaching each other.

A group is a collection of programs that can all communicate via pipes either directly or indirectly.
The programs you identified just a moment ago are all part of the same group.
Now, they would like you to determine the total number of groups.

In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6,
and the other consisting solely of program 1.

How many groups are there in total?
"""


class Tree2(Tree):

    def get_all_groups(self) -> List[Set[Node]]:
        groups = []
        seen = set()

        for _, node in self.nodes.items():
            if node not in seen:
                group = set()
                self.get_group(node, group)
                groups.append(group)
                seen = seen.union(group)

        return groups


class Part02Test(Part01Test):

    def test_all_groups(self):
        tree = Tree2.from_multilines(self.literals)

        groups = tree.get_all_groups()

        self.assertEqual(len(groups), 2)


def part02(fpath):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part02Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    with open(fpath, 'r') as f:
        tree = Tree2.from_multilines(f.read())

    groups = tree.get_all_groups()
    print('- Part02 Answer:', len(groups))


if __name__ == '__main__':
    part01('day12_input.txt')  # 169
    part02('day12_input.txt')  # 179
