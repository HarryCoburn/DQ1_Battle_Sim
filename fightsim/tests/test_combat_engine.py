import unittest
from ..models.combat_engine import CombatEngine
from ..models.spells import SpellType, SpellFailureReason
from ..common.messages import HerbFailureReason, HerbResult, EnemyActions

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
        
    def test_player_casts_heal_success(self):
        """Test healing when heal_max allows full heal amount"""
        self.combat_engine.randomizer.sequence = [15]  # Roll 15 HP
        
        result = self.combat_engine.player_casts_heal(SpellType.HEAL, heal_max=50)
        
        assert result.success == True
        assert result.amount == 15  # Got full random amount
        assert result.reason == None

    def test_player_casts_heal_capped_by_heal_max(self):
       """Test healing when heal_max caps the amount"""
       self.combat_engine.randomizer.sequence = [15]  # Roll 15 HP
        
       result = self.combat_engine.player_casts_heal(SpellType.HEAL, heal_max=5)
        
       assert result.success == True
       assert result.amount == 5  # Capped at heal_max
       assert result.reason == None

    def test_player_casts_heal_at_max_hp(self):
        """Test healing fails when already at max HP"""
        result = self.combat_engine.player_casts_heal(SpellType.HEAL, heal_max=0)
        
        assert result.success == False
        assert result.amount == 0
        assert result.reason == SpellFailureReason.HEALED_AT_MAX_HP

    def test_player_casts_hurt_success(self):
        self.combat_engine.randomizer.sequence = [15] 

        result = self.combat_engine.player_casts_hurt(SpellType.HURT, 0)

        assert result.success == True
        assert result.amount == 15
        assert result.reason == None

    def test_player_casts_hurt_enemy_resists(self):
        self.combat_engine.randomizer.sequence = [15] 

        result = self.combat_engine.player_casts_hurt(SpellType.HURT, 17)

        assert result.success == False
        assert result.amount == 0
        assert result.reason == SpellFailureReason.ENEMY_RESISTED_HURT

    def test_player_casts_sleep_success(self):
        self.combat_engine.randomizer.sequence = [17]
        
        result = self.combat_engine.player_casts_sleep(SpellType.SLEEP, 0, 16) 

        assert result.success == True

    def test_player_casts_sleep_enemy_already_asleep(self):
        result = self.combat_engine.player_casts_sleep(SpellType.SLEEP, 1, 16) 

        assert result.success == False
        assert result.reason == SpellFailureReason.ENEMY_ALREADY_ASLEEP

    def test_player_casts_sleep_enemy_resists(self):
        self.combat_engine.randomizer.sequence = [0, 16]
        
        result = self.combat_engine.player_casts_sleep(SpellType.SLEEP, 0, 16) 

        assert result.success == False
        assert result.reason == SpellFailureReason.ENEMY_RESISTED_SLEEP

    def test_player_casts_spellstop_success(self):
        self.combat_engine.randomizer.sequence = [17]
        
        result = self.combat_engine.player_casts_stopspell(SpellType.STOPSPELL, False, 16) 

        assert result.success == True

    def test_player_casts_spellstop_enemy_already_spellstopped(self):
        result = self.combat_engine.player_casts_stopspell(SpellType.STOPSPELL, True, 16) 

        assert result.success == False
        assert result.reason == SpellFailureReason.ENEMY_ALREADY_SPELLSTOPPED

    def test_player_casts_spellstop_enemy_resists(self):
        self.combat_engine.randomizer.sequence = [0, 16]
        
        result = self.combat_engine.player_casts_stopspell(SpellType.STOPSPELL, False, 16) 

        assert result.success == False
        assert result.reason == SpellFailureReason.ENEMY_RESISTED_SPELLSTOP

    def test_resolve_herb_healing_success(self):
        self.combat_engine.randomizer.sequence = [12]

        result = self.combat_engine.resolve_herb_healing(10, 999)

        assert result.success == True
        assert result.healing == 12

    def test_resolve_herb_healing_max_hp(self):
        self.combat_engine.randomizer.sequence = [12]

        result = self.combat_engine.resolve_herb_healing(999, 999)

        assert result.success == False
        assert result.healing == 0
        assert result.reason == HerbFailureReason.MAX_HP

    def test_resolve_herb_healing_reduce_healing(self):
        self.combat_engine.randomizer.sequence = [12]

        result = self.combat_engine.resolve_herb_healing(996, 999)

        assert result.success == True
        assert result.healing == 3

    def test_resolve_enemy_attack_normal(self):

        result = self.combat_engine.resolve_enemy_attack(20, 5)

        assert result.damage >= 4
        assert result.damage <= 9

    def test_resolve_enemy_attack_weak(self):

        result = self.combat_engine.resolve_enemy_attack(5, 20)

        assert result.damage >= 0
        assert result.damage <= 1

    def test_enemy_casts_hurt_stopped(self):
        result = self.combat_engine.enemy_casts_hurt(EnemyActions.HURT, False, True)

        assert result.success == False
        assert result.reason == SpellFailureReason.ENEMY_SPELLSTOPPED

    def test_enemy_casts_hurt_success_no_defense(self):
        result = self.combat_engine.enemy_casts_hurt(EnemyActions.HURT, False, False)

        assert result.success == True
        assert result.amount >= 0
        assert result.reason == None

    def test_enemy_casts_hurt_success_with_defense(self):
        result = self.combat_engine.enemy_casts_hurt(EnemyActions.HURT, True, False)

        assert result.success == True
        assert result.amount >= 0
        assert result.reason == None

    def test_enemy_casts_breathes_fire_success_no_defense(self):
        result = self.combat_engine.enemy_breathes_fire(EnemyActions.FIRE, False)

        assert result.success == True
        assert result.amount >= 0
        assert result.reason == None

    def test_enemy_breathes_fire_success_with_defense(self):
        result = self.combat_engine.enemy_breathes_fire(EnemyActions.FIRE, True)

        assert result.success == True
        assert result.amount >= 0
        assert result.reason == None