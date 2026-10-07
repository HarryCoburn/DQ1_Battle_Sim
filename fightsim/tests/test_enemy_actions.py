import unittest
from fightsim.common.enemy_actions import EnemyActions


class TestEnemyActionsEnum(unittest.TestCase):
    def test_enum_members_exist(self):
        """Ensure all expected members are defined in EnemyActions."""
        expected_members = {
            'ATTACK', 'HEAL', 'HURT', 'SLEEP', 'STOPSPELL',
            'FIRE', 'HEALMORE', 'HURTMORE', 'STRONGFIRE'
        }
        actual_members = {member.name for member in EnemyActions}
        self.assertEqual(actual_members, expected_members)

    def test_enum_auto_values(self):
        """Test that enum values are unique and auto-assigned."""
        values = {member.value for member in EnemyActions}
        self.assertEqual(len(values), len(EnemyActions))

if __name__ == '__main__':
    unittest.main()
