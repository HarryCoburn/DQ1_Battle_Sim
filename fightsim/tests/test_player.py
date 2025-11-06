import unittest
from unittest.mock import patch
from ..models.player import player_factory

class TestPlayer(unittest.TestCase):
    """ Unit tests for the Player class """
    def setUp(self):
        self.player = player_factory()
        from ..models.enemy import enemy_instances
        self.enemy = enemy_instances["slime"]

    def test_player_attack_normal_hit(self):
        results = self.player.attack(self.enemy)
        # enemy_agility is 3
        # attack_num is 4 (Str) + 0 (unarmed)
        # Unarmed level 1 attack against slime is 1 or 0 damage.
        self.assertTrue(results.damage >= 0 and results.damage <= 1)
        
    
    @patch("fightsim.models.player.Player.did_crit")
    @patch("fightsim.models.enemy.Enemy.did_dodge")
    def test_player_attack_critical_hit(self, mock_did_dodge, mock_did_crit):
        mock_did_crit.return_value = True
        mock_did_dodge.return_value = False

        # enemy_agility is 3
        # attack_num is 4 (Str) + 0 (unarmed)
        # critical hit
        # Unarmed level 1 attack against slime with a crit is between 2 and 4 damage.
        results = self.player.attack(self.enemy)
        self.assertTrue(results.crit)
        self.assertTrue(results.hit)
        self.assertTrue(results.damage >= 2 and results.damage <= 4)
        
    @patch("fightsim.models.player.Player.calculate_attack_damage")
    def test_player_attack_returns_exact_number(self, mock_calculate_attack_damage):
        mock_calculate_attack_damage.return_value = 8
        results = self.player.attack(self.enemy)
        # Force a damage of 8
        self.assertTrue(results.damage == 8)

if __name__ == '__main__':
    unittest.main()