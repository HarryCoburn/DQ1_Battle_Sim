from ..common.randomizer import Randomizer
from dataclasses import dataclass

@dataclass
class AttackResult:
    crit: bool
    dodge: bool
    damage: int
    hit: bool

class CombatEngine:
    def __init__(self):
        self.CRIT_CHANCE = 32
        pass    

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
        return Randomizer.randint(1, self.CRIT_CHANCE) == 1
    
    def enemy_did_dodge(self, dodge_chance):
        return Randomizer.randint(1, 64) <= dodge_chance

    def calculate_player_attack_damage(self, crit, enemy_agility, player_strength, player_weapon):
        player_computed_attack = player_strength + player_weapon
        if crit:
            low, high = self.player_crit_range(player_computed_attack)
        else:
            low, high = self.player_damage_range(player_computed_attack, enemy_agility)
        return Randomizer.randint(low, high)

    def resolve_player_attack(self, player_strength, player_weapon, enemy_agility, enemy_dodge_chance, enemy_blocks_crits):
        crit = enemy_blocks_crits is False and self.player_did_crit()
        dodge = self.enemy_did_dodge(enemy_dodge_chance)
        damage = self.calculate_player_attack_damage(crit, enemy_agility, player_strength, player_weapon)

        return AttackResult(
            crit=crit, dodge=dodge, damage=damage, hit=not (dodge and not crit)
        )