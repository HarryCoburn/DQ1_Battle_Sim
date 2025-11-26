import unittest
from ..models.combat_engine import CombatEngine
from dataclasses import dataclass
from ..models.spells import SpellType, SpellFailureReason

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



class TestCombatEngine(unittest.TestCase):
    def setUp(self):
        self.combat_engine = CombatEngine(FakeRandomizer())
        

    def test_combat_engine_attack_calculation(self):
        # No crit, no dodge
        
        self.combat_engine.randomizer.sequence = [2,10,20]

        result = self.combat_engine.resolve_player_attack(
            player_strength=50,
            player_weapon=10,
            enemy_agility=3,
            enemy_dodge_chance=1,
            enemy_blocks_crits=False
        )
        
        # Result is an AttackResult
        
        assert result.damage == 20
        assert result.hit == True
        assert result.crit == False 

    def test_combat_engine_attack_calculation_crit(self):
        # crit, no dodge
        
        self.combat_engine.randomizer.sequence = [1,10]

        result = self.combat_engine.resolve_player_attack(
            player_strength=50,
            player_weapon=10,
            enemy_agility=30,
            enemy_dodge_chance=5,
            enemy_blocks_crits=False
        )
        
        # Result is an AttackResult
        assert result.damage == 45
        assert result.hit == True
        assert result.crit == True  # or True depending on your logic

    def test_combat_engine_attack_dodged(self):
        # No crit, dodge
        
        self.combat_engine.randomizer.sequence = [2,1]

        result = self.combat_engine.resolve_player_attack(
            player_strength=50,
            player_weapon=10,
            enemy_agility=30,
            enemy_dodge_chance=5,
            enemy_blocks_crits=False
        )       
                
        assert result.hit == False
        assert result.dodge == True  # or True depending on your logic

    def test_combat_engine_crits_cancel_dodge(self):

        # No crit, dodge
        
        self.combat_engine.randomizer.sequence = [1,1]

        result = self.combat_engine.resolve_player_attack(
            player_strength=50,
            player_weapon=10,
            enemy_agility=30,
            enemy_dodge_chance=5,
            enemy_blocks_crits=False
        )       
                
        assert result.hit == True
        assert result.dodge == True  # or True depending on your logic
        assert result.crit == True

    def test_resolve_player_magic_when_successful(self):
        result = self.combat_engine.resolve_player_magic(SpellType.HEAL, 10, False)
        assert result.success == True
        assert result.reason == None

    def test_resolve_player_magic_when_not_enough_mp(self):
        result = self.combat_engine.resolve_player_magic(SpellType.HEAL, 0, False)
        assert result.success == False
        assert result.reason == SpellFailureReason.NOT_ENOUGH_MP

    def test_resolve_player_magic_when_spellstopped(self):
        result = self.combat_engine.resolve_player_magic(SpellType.HEAL, 10, True)
        assert result.success == False
        assert result.reason == SpellFailureReason.PLAYER_SPELLSTOPPED
        