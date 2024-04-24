import unittest
from unittest.mock import patch
from ..common.randomizer import Randomizer

class TestRandomizer(unittest.TestCase):
    """ Unit tests for the Randomizer class. """

    def test_randint(self):
        low, high = 1, 10
        results = {Randomizer.randint(low, high) for _ in range(1000)}
        self.assertTrue(all(low <= num <= high for num in results))
        self.assertTrue(len(results) > 1)  # Check that we have a range of outputs

    def test_chance(self):
        # Test by patching random.random to control its output
        with patch('random.random', return_value=0.5):
            self.assertTrue(Randomizer.chance(0.6))
            self.assertFalse(Randomizer.chance(0.4))

    def test_choice(self):
        seq = [1, 2, 3, 4, 5]
        chosen = Randomizer.choice(seq)
        self.assertIn(chosen, seq)

        # Test that it raises an exception with an empty list
        with self.assertRaises(IndexError):
            Randomizer.choice([])