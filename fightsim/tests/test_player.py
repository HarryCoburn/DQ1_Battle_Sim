import unittest
# from unittest.mock import patch
from ..models.player import player_factory
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

class TestPlayer(unittest.TestCase):
    """ Unit tests for the Player class """
    def setUp(self):        
        self.player = player_factory(CombatEngine(FakeRandomizer()))
        self.player.equip_weapon("Copper Sword") # Equip copper sword
        self.enemy = create_enemy('slime', combat_engine=CombatEngine)

    def test_player_attack_normal_hit(self):
        self.player.combat_engine.randomizer.sequence = [2, 10, 20]

        # First check that the player's paramters are correct for passing in.
        assert self.player.weapon.modifier == 10
        assert self.enemy.agility == 3
        assert self.enemy.dodge == 1

        # Claude wants to force a strength of 50. Technically, a level 10
        # player would have, at maximum, 35 strength or lower, depending on the name of the player.
        # Therefore, since we are forcing a result anyway, we shall ignore this.

        results = self.player.attack(self.enemy)
        # Old test
        # enemy_agility is 3
        # attack_num is 4 (Str) + 0 (unarmed)
        # Unarmed level 1 attack against slime is 1 or 0 damage.
        # self.assertTrue(results.damage >= 0 and results.damage <= 1)
        assert results.damage == 20
        assert results.hit == True
        assert results.crit == False   
  

if __name__ == '__main__':
    unittest.main()