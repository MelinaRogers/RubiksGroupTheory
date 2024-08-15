import unittest
from rubiks_corner_analyzer import RubiksCube

class TestRubiksCube(unittest.TestCase):
    def setUp(self):
        self.cube = RubiksCube()

    def test_initial_state(self):
        self.assertTrue(self.cube.is_solved())
        self.assertEqual(self.cube.cycle_structure(), [1])
        self.assertEqual(self.cube.orientation_sum(), 0)

    def test_scramble(self):
        self.cube.scramble(100)
        self.assertFalse(self.cube.is_solved())

    def test_cycle_structure(self):
        # Force a specific permutation
        self.cube.corners = [(1, 0), (2, 0), (0, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        self.assertEqual(self.cube.cycle_structure(), [3])

    def test_orientation_sum(self):
        # Force specific orientations
        self.cube.corners = [(i, 1) for i in range(8)]
        self.assertEqual(self.cube.orientation_sum(), 2)  # 8 mod 3 = 2

if __name__ == '__main__':
    unittest.main()