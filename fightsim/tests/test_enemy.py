import unittest
from ..models.combat_engine import CombatEngine
from ..models.enemy import create_enemy

class FakeRandomizer:
    """A deterministic randomizer for testing"""
    def __init__(self, fixed_value=None, sequence=None):
        self.fixed_value = fixed_value
        self.sequence = sequence or []
        self.call_count = 0
    
    def randint(self, low, high):
        if self.sequence:
            # Return values from sequence
            if self.call_count >= len(self.sequence):
                return (low + high) // 2    
            value = self.sequence[self.call_count % len(self.sequence)]
            self.call_count += 1
            return value
        elif self.fixed_value is not None:
            return self.fixed_value
        else:
            # Fallback to midpoint
            return (low + high) // 2
        

class TestEnemy(unittest.TestCase):
    def test_enemy_independence(self):
        combat_engine = CombatEngine(FakeRandomizer())

        enemy = create_enemy('slime', combat_engine)

        assert enemy.name == "Slime"