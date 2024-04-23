import unittest
from ..common.messages import ObserverMessages, EnemyActions


class TestObserverMessagesEnum(unittest.TestCase):
    def test_enum_members_exist(self):
        """Test that all expected enum members exist."""
        expected_members = {
            'OUTPUT_CHANGE', 'OUTPUT_CLEAR', 'ENEMY_CHANGE',
            'PLAYER_HP_CHANGE', 'WEAPON_CHANGE', 'SHIELD_CHANGE',
            'ARMOR_CHANGE', 'RESET_GAME'
        }
        actual_members = {member.name for member in ObserverMessages}
        self.assertEqual(actual_members, expected_members)

    def test_enum_auto_values(self):
        """Test that enum values are unique and auto-assigned."""
        values = {member.value for member in ObserverMessages}
        self.assertEqual(len(values), len(ObserverMessages))

    def test_enum_descriptions_are_present(self):
        """ Test that all the enums have a non-default description """
        for member in ObserverMessages:
            with self.subTest(member=member):
                description = member.description()
                self.assertNotEqual(description, "No description available.",
                                    f"{member.name} should have a custom description.")


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

    def test_enum_descriptions_are_present(self):
        """ Test that all the enums have a non-default description """
        for member in EnemyActions:
            with self.subTest(member=member):
                description = member.description()
                self.assertNotEqual(description, "No description available.",
                                    f"{member.name} should have a custom description.")

# Add more tests as needed for specific logic or value checks if values are manually assigned.

if __name__ == '__main__':
    unittest.main()
