"""
--- Day 3: Spiral Memory ---
You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1
and then counting up while spiraling outward.
For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped),
requested data must be carried back to square 1
(the location of the only access port for this memory system)
by programs that can only move up, down, left, or right.
They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square
identified in your puzzle input all the way to the access port?
"""

"""
Pattern:

x                 sqrt(x)       layer(x)
========================================
1                 1                   0
[2, 9]        1 < x <= 3              1
[10, 25]      3 < x <= 5              2
[26, 49]      5 < x <= 7              3
[50, 81]      7 < x <= 9              4
...
"""
import math
import unittest
from typing import Tuple


def find_layer_of(x: int) -> int:
    """
    Find the layer the value x belong to.
    Params:
        x: should be larger than 0
    """

    if x < 0:
        raise ValueError('x should be larger than 0.')

    sqrt = math.sqrt(x)

    return math.ceil(0.5 * (sqrt - 1.0))


def find_head_of(layer: int) -> int:
    """
    Find starting value of the layer.
    Params:
        layer: should be equal to or larger than 0.
    """
    if layer < 0:
        raise ValueError

    if layer == 0:
        return 1
    return  int(1 + (2 * (layer - 1) + 1) ** 2)


def find_coordinate_of(x: int) -> Tuple[int, int]:
    """
    1 -> (0, 0)
    3 -> (1, 1)
    10 -> (2, -1)
    last value of the layer -> (-layer, layer)
    """
    layer = find_layer_of(x)
    if layer == 0:
        return (0, 0)
    head = find_head_of(layer)
    sidelength = layer * 2
    residual = x - head
    nth_side = residual // sidelength
    if nth_side >= 4:
        raise ValueError('nth_side should not be larger than 3.')
    modulo = residual % sidelength

    i = layer * (1 if nth_side <= 1 else -1)
    j = layer * (1 if nth_side == 1 or nth_side == 2 else -1)
    if nth_side % 2 == 0:
        sign = 1 if nth_side == 0 else -1
        return (i, j + sign * (1 + modulo))
    else:
        sign = -1 if nth_side == 1 else 1
        return (i + sign * (1 + modulo), j)


def manhatten_distance(coordinate: Tuple[int, int]) -> int:
    return sum(abs(v) for v in coordinate)


class Part01Test(unittest.TestCase):

    def test_find_head(self):
        self.assertEqual(find_head_of(0), 1)
        self.assertEqual(find_head_of(1), 2)
        self.assertEqual(find_head_of(2), 10)
        self.assertEqual(find_head_of(3), 26)

    def test_find_layer(self):
        self.assertEqual(find_layer_of(1), 0)
        self.assertEqual(find_layer_of(9), 1)
        self.assertEqual(find_layer_of(8), 1)
        self.assertEqual(find_layer_of(25), 2)
        self.assertEqual(find_layer_of(26), 3)

    def test_coordinate(self):
        self.assertEqual(find_coordinate_of(1), (0, 0))
        self.assertEqual(find_coordinate_of(9), (1, -1))
        self.assertEqual(find_coordinate_of(12), (2, 1))
        self.assertEqual(find_coordinate_of(13), (2, 2))
        self.assertEqual(find_coordinate_of(14), (1, 2))
        self.assertEqual(find_coordinate_of(20), (-2, -1))
        self.assertEqual(find_coordinate_of(21), (-2, -2))
        self.assertEqual(find_coordinate_of(22), (-1, -2))

    def test_manhatten_distance(self):
        self.assertEqual(manhatten_distance(find_coordinate_of(1)), 0)
        self.assertEqual(manhatten_distance(find_coordinate_of(12)), 3)
        self.assertEqual(manhatten_distance(find_coordinate_of(23)), 2)
        self.assertEqual(manhatten_distance(find_coordinate_of(1024)), 31)


def part01(x):

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part01Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    coord = find_coordinate_of(x)
    print('- Part01 Answer:', manhatten_distance(coord))


"""
--- Part Two ---
As a stress test on the system,
the programs here clear the grid and then store the value 1 in square 1.
Then, in the same allocation order as shown above,
they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors
and stores the sum of their values, 4.

Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change.
Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
What is the first value written that is larger than your puzzle input?
"""


def get_neighbers(coord: Tuple[int, int], nth: int):
    neibors = []
    if coord == (0, 0):
        return [(0, 0)]
    if nth == 0:
        neibors.append((coord[0], coord[1] - 1))
        neibors.extend([(coord[0] - 1, coord[1] + i) for i in [-1, 0, 1]])
    elif nth == 1:
        neibors.append((coord[0] + 1, coord[1]))
        neibors.extend([(coord[0] + i, coord[1] - 1) for i in [-1, 0, 1]])
    elif nth == 2:
        neibors.append((coord[0], coord[1] + 1))
        neibors.extend([(coord[0] + 1, coord[1] + i) for i in [-1, 0, 1]])
    else:
        neibors.append((coord[0] - 1, coord[1]))
        neibors.extend([(coord[0] + i, coord[1] + 1) for i in [-1, 0, 1]])

    return neibors


def get_square_value(upper: int):

    i = 2
    seen_coords = {(0, 0): 1}
    seen_layers = {0: 1}
    while i < upper:
        layer = find_layer_of(i)
        sidelength = layer * 2
        head = seen_layers[layer] if layer in seen_layers else find_head_of(layer)
        residual = 1 + i - head
        nth_side = residual // sidelength
        coord = find_coordinate_of(i)
        neibors = get_neighbers(coord, nth_side)
        v = sum(seen_coords[nb] for nb in neibors if nb in seen_coords)

        if v >= upper:
            return v

        seen_coords[coord] = v
        i += 1

    raise ValueError


class Part02Test(unittest.TestCase):

    def test_neibors(self):
        self.assertEqual(set(get_neighbers((4, -1), 0)), {(4, -2), (3, -2), (3, -1), (3, 0)})
        self.assertEqual(set(get_neighbers((-1, 1), 2)), {(-1, 2), (0, 0), (0, 1), (0, 2)})
        self.assertEqual(set(get_neighbers((-1, 2), 1)), {(-2, 1), (-1, 1), (0, 1), (0, 2)})
        self.assertEqual(set(get_neighbers((-3, -3), 3)), {(-4, -3), (-4, -2), (-3, -2), (-2, -2)})

    def test_square_value(self):
        self.assertEqual(get_square_value(13), 23)
        self.assertEqual(get_square_value(57), 57)
        self.assertEqual(get_square_value(329), 330)


def part02(upper: int):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Part02Test))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

    print('- Part02 Answer:', get_square_value(upper))


if __name__ == '__main__':
    part01(361527)  # 326
    part02(361527)  # 363010
