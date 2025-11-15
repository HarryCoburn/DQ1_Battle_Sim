from ..common.randomizer import Randomizer
from dataclasses import dataclass
from .spells import SpellType, SpellResult
from ..common.messages import SpellFailureReason, HerbFailureReason, HerbResult, EnemyActions
@dataclass
class AttackResult:
    crit: bool = False
    dodge: bool = False
    damage: int
    hit: bool = True

class CombatEngine:
    def __init__(self, randomizer):
        self.randomizer = randomizer if randomizer is not None else Randomizer()
        self.CRIT_CHANCE = 32
        self.ENEMY_SLEEP_ROUNDS = 2            

        self.HEAL_RANGES = {
            SpellType.HEAL: (10, 17),
            SpellType.HEALMORE: (58, 85)
        }

        self.HURT_RANGES = {
            SpellType.HURT: (5, 12),
            SpellType.HURTMORE: (58, 65)
        }

        self.HERB_RANGE = (23, 30)

    # Player Attack

    def player_damage_range(self, player_attack, enemy_agility):
        """
        Returns a possible damage range for a normal player_attack aenemy_aa tuple in the form (min, max)
        min must be at least 0, max can be no lower than 1
        """
        return max(((player_attack - enemy_agility // 2) // 4), 0), max(
            ((player_attack - enemy_agility // 2) // 2), 1
        )

    def player_crit_range(self, player_attack):
        """
        Returns a possible critical damage range for a normal attack as a tuple in the form (min, max)
        min must be at least 0, max can be no lower than 1
        """
        return max((player_attack // 2), 0), max(player_attack, 1)
    
    def player_did_crit(self):
        return self.randomizer.randint(1, self.CRIT_CHANCE) == 1
    
    def enemy_did_dodge(self, dodge_chance):
        return self.randomizer.randint(1, 64) <= dodge_chance

    def calculate_player_attack_damage(self, crit, enemy_agility, player_strength, player_weapon):
        player_computed_attack = player_strength + player_weapon
        if crit:
            low, high = self.player_crit_range(player_computed_attack)
        else:
            low, high = self.player_damage_range(player_computed_attack, enemy_agility)
        return self.randomizer.randint(low, high)

    def resolve_player_attack(self, player_strength, player_weapon, enemy_agility, enemy_dodge_chance, enemy_blocks_crits):
        crit = enemy_blocks_crits is False and self.player_did_crit()
        dodge = self.enemy_did_dodge(enemy_dodge_chance)
        damage = self.calculate_player_attack_damage(crit, enemy_agility, player_strength, player_weapon)

        return AttackResult(
            crit=crit, dodge=dodge, damage=damage, hit=not (dodge and not crit)
        )
    
    # Player Magic

    def resolve_player_magic(self, spell, player_mp, player_is_spellstopped):
        if player_mp < spell.value.mp_cost:
            return SpellResult(
                spell_name=spell, success=False, amount=0, reason=SpellFailureReason.NOT_ENOUGH_MP
            )
        if player_is_spellstopped:
            return SpellResult(
                spell_name=spell, success=False, amount=0, reason=SpellFailureReason.PLAYER_SPELLSTOPPED
            )
        return SpellResult(spell_name=spell, success=True, amount=0)

    def player_casts_heal(self, spell, heal_max):
        heal_amount = min(heal_max, self.randomizer.randint(*self.HEAL_RANGES[spell]))  
        if heal_amount == 0:
            return SpellResult(spell_name=spell, success=False, amount=0, reason=SpellFailureReason.HEALED_AT_MAX_HP)
        return SpellResult(spell_name=spell, success=True, amount=heal_amount, reason=None)

    def player_casts_hurt(self, spell, enemy_hurt_resist):
        hurt_range = self.HURT_RANGES[spell]
        hurt_amount = self.randomizer.randint(*hurt_range)
        if self.randomizer.randint(1, 16) <= enemy_hurt_resist:
            return SpellResult(spell_name=spell, success=False, amount=0, reason=SpellFailureReason.ENEMY_RESISTED_HURT)
        return SpellResult(spell_name=spell, success=True, amount=hurt_amount, reason=None)

    def player_casts_sleep(self, spell, enemy_sleep_count, enemy_sleep_resistance):
        if enemy_sleep_count > 0:  # enemy already asleep
            return SpellResult(spell_name="Sleep", success=False, reason=SpellFailureReason.ENEMY_ALREADY_ASLEEP)
        if self.randomizer.randint(1, 16) <= enemy_sleep_resistance:  # enemy resists sleep
            return SpellResult(spell_name="Sleep", success=False, reason=SpellFailureReason.ENEMY_RESISTED_SLEEP)
        return SpellResult(spell_name=spell, success=True, amount=self.ENEMY_SLEEP_ROUNDS, reason=None)
    
    def player_casts_stopspell(self, spell, is_spellstopped, enemy_spellstop_resistance):
        if is_spellstopped:
            return SpellResult(spell_name=spell, success=False, reason=SpellFailureReason.ENEMY_ALREADY_SPELLSTOPPED)
        if self.randomizer.randint(1, 16) <= enemy_spellstop_resistance:  
            return SpellResult(spell_name="Sleep", success=False, reason=SpellFailureReason.ENEMY_RESISTED_SPELLSTOP)
        return SpellResult(spell_name=spell, success=True, amount=0, reason=None)
    
    # Player herbs
    def player_herb_healing(self, current_hp, max_hp):
        if current_hp >= max_hp:
            return HerbResult(success=False, healing=0, reason=HerbFailureReason.MAX_HP)
        herb_hp = self.randomizer.randint(*self.HERB_RANGE)
        actual_hp_gained = min(herb_hp, max_hp - current_hp)

        return HerbResult(success=True, healing=actual_hp_gained)

    #
    # ENEMY
    #    

    def enemy_flees(self, enemy_strength, player_strength):
        return player_strength > enemy_strength * 2 and self.randomizer.randint(1,4) == 4
    
    def enemy_wakes_up(self):
        return Randomizer.randint(1, 3) == 3
    
    def resolve_enemy_attack(self, enemy_strength, player_defense):
        if player_defense > enemy_strength:
            enemy_damage_dealt = Randomizer.randint(*self.weak_damage_range(enemy_strength))
        else:
            enemy_damage_dealt = Randomizer.randint(*self.normal_damage_range(enemy_strength, player_defense))
        return AttackResult(damage=enemy_damage_dealt)
    
    def weak_damage_range(self, enemy_strength):
        """ Returns a damage tuple for a weak attack. """
        return 0, ((enemy_strength + 4) // 6)
    
    def normal_damage_range(self, enemy_strength, player_defense):
        """ Returns a damage tuple for a strong attack. """
        return ((enemy_strength - player_defense // 2) // 4), ((enemy_strength - player_defense // 2) // 2)
    
    def enemy_casts_hurt(self, action, player_defense, enemy_spell_stopped):
        if enemy_spell_stopped:
            return SpellResult(action.description, False, 0, SpellFailureReason.ENEMY_ALREADY_SPELLSTOPPED)
        
        hurt_high = []
        hurt_low = []

        if action == EnemyActions.HURT:
            hurt_high = [3, 10]
            hurt_low = [2, 6]
        elif action == EnemyActions.HURTMORE:
            hurt_high = [30,45] 
            hurt_low = [20,30]

        if player_defense:
            hurt_dmg = Randomizer.randint(*hurt_low)
        else:
            hurt_dmg = Randomizer.randint(*hurt_high)

        return SpellResult(action.description, True, hurt_dmg)
    
    def enemy_breathes_fire(self, action, reduce_fire_damage):        
        
        fire_high = []
        fire_low = []

        if action == EnemyActions.FIRE:
            fire_high = [16, 23]
            fire_low = [10, 14]
        elif action == EnemyActions.STRONGFIRE:
            fire_high = [65,72] 
            fire_low = [42,48]

        if reduce_fire_damage:
            fire_dmg = Randomizer.randint(*fire_low)
        else:
            fire_dmg = Randomizer.randint(*fire_high)

        return SpellResult(action.description, True, fire_dmg)