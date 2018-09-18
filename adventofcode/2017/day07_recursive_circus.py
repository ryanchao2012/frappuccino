"""
--- Day 7: Recursive Circus ---
Wandering further through the circuits of the computer,
you come upon a tower of programs that have gotten themselves into a bit of trouble.
A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large tower.

One program at the bottom supports the entire tower.
It's holding a large disc, and on the disc are balanced several more sub-towers.
At the bottom of these sub-towers, standing on the bottom disc, are other programs,
each holding their own disc, and so on. At the very tops of these sub-sub-sub-...-towers,
many programs stand simply keeping the disc below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these towers.
You ask each program to yell out their name, their weight,
and (if they're holding a disc) the names of the programs immediately above them balancing on that disc.
You write this information down (your puzzle input).
Unfortunately, in their panic, they don't do this in an orderly fashion;
by the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth
In this example, tknk is at the bottom of the tower (the bottom program),
and is holding up ugml, padx, and fwft.
Those programs are, in turn, holding up other programs;
in this example, none of those programs are holding up any other programs,
and are all the tops of their own towers. (The actual tower balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is correct.
What is the name of the bottom program?
"""


import re
import unittest
from functools import lru_cache
from typing import Dict, List, Optional, Tuple


class Node:

    __slots__ = ('name', 'value', 'parent', 'childs', 'weight')

    def __init__(self, name: str,
                 value: Optional[int] = None,
                 parent: Optional['Node'] = None,
                 childs: Optional[List['Node']] = None):
        self.name = name
        self.value = value
        self.weight = 0
        self.parent = None
        self.childs = set()
        self.set_parent(parent)
        self.add_childs(childs or [])

    def set_parent(self, parent: Optional['Node']) -> None:
        if parent is None:
            return
        if self.parent is None:
            self.parent = parent
        elif self.parent.name != parent.name:
            raise ValueError('Parent already existed.')

    def set_value(self, value: int) -> None:
        self.value = value or self.value

    def add_childs(self, childs: List['Node']) -> None:
        for ch in childs:
            ch.set_parent(self)
        self.childs = self.childs.union(set(childs))

    def __str__(self):
        return (f'Parent[{self.parent.name + ":" + str(self.parent.value) if self.parent is not None else None}]'
                f' > {self.name}:{self.value}'
                f' >> Childs[{set([":".join([ch.name, str(ch.value)]) for ch in self.childs]) or "{}"}]')

    def __repr__(self):
        return str(self)


def node_parser(literal: str):
    mix = literal.split('->')
    m = re.match(r'(\w+) \((\d+)\)', mix[0])
    name = m.group(1)
    value = int(m.group(2))
    if len(mix) == 2:
        children = [ch.strip() for ch in mix[1].split(',')]
    else:
        children = []

    return name, value, children


class Tree:
    def __init__(self):
        self.nodes = {}
        self.root = None

    def add_node(self, node: Node) -> None:
        for ch in node.childs:
            self.add_node(ch)

        if node.name in self.nodes:
            this = self.get_node(node.name)
            this.set_value(node.value)
            this.add_childs(node.childs)
        else:
            self.nodes[node.name] = node

    def get_node(self, name) -> Optional[Node]:
        return self.nodes.get(name, None)

    def get_roots(self) -> List[Node]:
        return [nd for name, nd in self.nodes.items() if nd.parent is None]


class Part01Test(unittest.TestCase):
    def test_node(self):
        root1 = Node('root', 0)
        child1 = Node('child1', 101)
        child2 = Node('child2', 201)
        child3 = Node('child1', 101)
        child4 = Node('child2', 201)
        node1 = Node('node1', 5566, parent=root1, childs=[child1])
        node2 = Node('node1', 5566, parent=root1, childs=[child3])
        self.assertEqual(str(child4), str(child2))
        self.assertEqual(str(node1), str(node2))

    def test_parser(self):
        literal1 = 'luhxcq (68)'

        actual = node_parser(literal1)

        self.assertEqual(actual, ('luhxcq', 68, []))

        literal2 = 'iedrlkp (176) -> xiwnu, gezqw'
        actual = node_parser(literal2)
        self.assertEqual(actual, ('iedrlkp', 176, ['xiwnu', 'gezqw']))

    def test_tree(self):
        literal = (
            """
            pbga (66)
            xhth (57)
            ebii (61)
            havc (66)
            ktlj (57)
            fwft (72) -> ktlj, cntj, xhth
            qoyq (66)
            padx (45) -> pbga, havc, qoyq
            tknk (41) -> ugml, padx, fwft
            jptl (61)
            ugml (68) -> gyxo, ebii, jptl
            gyxo (61)
            cntj (57)
            """
        )
        tree = Tree()
        for line in literal.strip().split('\n'):
            name, value, ch = node_parser(line.strip())
            childs = [tree.get_node(c) if c in tree.nodes else Node(c) for c in ch]
            tree.add_node(Node(name, value, childs=childs))

        root = tree.get_roots()[0]
        self.assertEqual(root.name, 'tknk')


def part01(fpath):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    tree = Tree()
    with open(fpath, 'r') as f:
        for line in f:
            name, value, ch = node_parser(line.strip())
            childs = [tree.get_node(c) if c in tree.nodes else Node(c) for c in ch]
            tree.add_node(Node(name, value, childs=childs))
    print('- Part01 Answer:', [r.name for r in tree.get_roots()])


"""
--- Part Two ---
The programs explain the situation: they can't get down. Rather, they could get down,
if they weren't expending all of their energy trying to keep the tower balanced.
Apparently, one program has the wrong weight, and until it's fixed, they're stuck here.

For any program holding a disc, each program standing on that disc forms a sub-tower.
Each of those sub-towers are supposed to be the same weight, or the disc itself isn't balanced.
The weight of a tower is the sum of the weights of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii,
and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each match.
This means that the following sums must all be the same:

ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two.
Even though the nodes above ugml are balanced, ugml itself is too heavy:
it needs to be 8 units lighter for its stack to weigh 243 and keep the towers balanced.
If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?
"""


class Tree2(Tree):

    def balancing(self) -> int:
        pass

    @lru_cache()
    def sum_descendant_value(self, name: str):
        node = self.get_node(name)
        return sum(ch.value + self.sum_descendant_value(ch.name) for ch in node.childs)

    @lru_cache()
    def sum_balancing_value(self, name: str):
        node = self.get_node(name)
        sum_values = {ch.name: ch.value + self.sum_balancing_value(ch.name)
                      for ch in node.childs}
        if len(sum_values) == 0:
            return 0
        r = self.find_unbalanced(sum_values)
        if r is not None:
            mal_node, mal_value = r
            self.get_node(mal_node).weight = mal_value

        return sum(sum_values.values()) + sum(ch.weight for ch in node.childs)

    # XXX: ugly ...
    def find_unbalanced(self, values: Dict[str, int]) -> Optional[Tuple[str, int]]:
        seen = {}

        for k, v in values.items():
            if v in seen:
                seen[v].append(k)
            else:
                seen[v] = [k]
        if len(seen) <= 1:
            return None
        a = sorted([(k, v) for k, v in seen.items()], key=lambda x: len(x[1]))
        return a[0][1][0], a[1][0] - a[0][0]


class Part02Test(unittest.TestCase):

    literal = (
        """
        pbga (66)
        xhth (57)
        ebii (61)
        havc (66)
        ktlj (57)
        fwft (72) -> ktlj, cntj, xhth
        qoyq (66)
        padx (45) -> pbga, havc, qoyq
        tknk (41) -> ugml, padx, fwft
        jptl (61)
        ugml (68) -> gyxo, ebii, jptl
        gyxo (61)
        cntj (57)
        """
    )

    def build_tree(self):
        tree = Tree2()
        for line in self.literal.strip().split('\n'):
            name, value, ch = node_parser(line.strip())
            childs = [tree.get_node(c) if c in tree.nodes else Node(c) for c in ch]
            tree.add_node(Node(name, value, childs=childs))
        return tree

    def test_sum_descendant(self):
        tree = self.build_tree()

        self.assertEqual(tree.sum_descendant_value('tknk'), 737)
        self.assertEqual(tree.sum_descendant_value('ugml'), 183)
        self.assertEqual(tree.sum_descendant_value('padx'), 198)
        self.assertEqual(tree.sum_descendant_value('fwft'), 171)

    def test_balance(self):
        tree = self.build_tree()

        self.assertEqual(tree.sum_balancing_value('ugml'), 183)
        self.assertEqual(tree.sum_balancing_value('padx'), 198)
        self.assertEqual(tree.sum_balancing_value('fwft'), 171)
        self.assertEqual(tree.sum_balancing_value('tknk'), 729)


def part02(fpath):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part02Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    tree = Tree2()
    with open(fpath, 'r') as f:
        for line in f:
            name, value, ch = node_parser(line.strip())
            childs = [tree.get_node(c) if c in tree.nodes else Node(c) for c in ch]
            tree.add_node(Node(name, value, childs=childs))

    root = tree.get_roots()[0]
    balanced_value = tree.sum_balancing_value(root.name)
    mal_node = [node for name, node in tree.nodes.items() if node.weight != 0][0]

    print('- Balanced sum:', balanced_value)
    print('- Part02 Answer:', mal_node.value + mal_node.weight)


if __name__ == '__main__':
    part01('day07_input.txt')  # fbgguv
    part02('day07_input.txt')  # 1864
