import unittest
from ..models.combat_engine import CombatEngine

class TestCombatEngine(unittest.TestCase):
    def setUp(self):
        self.combat_engine = CombatEngine()

    def test_combat_engine_attack_calculation():
        # Given: A deterministic randomizer
        fake_random = FakeRandomizer(fixed_value=1)
        engine = CombatEngine(randomizer=fake_random)
        
        # When: Calculating an attack
        result = engine.resolve_attack(
            attacker_strength=50,
            attacker_weapon=10,
            defender_agility=30,
            defender_can_dodge=False,
            defender_blocks_crits=False
        )
        
        # Then: Result is deterministic and predictable
        assert result.damage == expected_value
        assert result.hit == True
        assert result.crit == False  # or True depending on your logic