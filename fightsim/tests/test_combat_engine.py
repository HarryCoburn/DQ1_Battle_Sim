import unittest
from ..models.combat_engine import CombatEngine

class FakeRandomizer:
    """A deterministic randomizer for testing"""
    def __init__(self, fixed_value=None, sequence=None):
        self.fixed_value = fixed_value
        self.sequence = sequence or []
        self.call_count = 0
    
    def randint(self, low, high):
        if self.sequence:
            # Return values from sequence
            value = self.sequence[self.call_count % len(self.sequence)]
            self.call_count += 1
            return value
        elif self.fixed_value is not None:
            return self.fixed_value
        else:
            # Fallback to midpoint
            return (low + high) // 2


class TestCombatEngine(unittest.TestCase):
    def setUp(self):
        self.combat_engine = CombatEngine(FakeRandomizer)

    def test_combat_engine_attack_calculation(self):
        # No crit, no dodge
        
        self.combat_engine.randomizer.sequence = [2,10,25]

        result = self.combat_engine.resolve_player_attack(
            player_strength=50,
            player_weapon=10,
            enemy_agility=30,
            enemy_dodge_chance=5,
            enemy_blocks_crits=False
        )
        
        # Result is an AttackResult
        
        assert result.damage == 25
        assert result.hit == True
        assert result.crit == False  # or True depending on your logic