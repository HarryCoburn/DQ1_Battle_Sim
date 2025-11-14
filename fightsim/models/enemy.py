import random
from dataclasses import dataclass, field
from typing import List, Optional
from .enemy_data import enemy_dict
from ..common.randomizer import Randomizer
from .combat_engine import CombatEngine
from ..common.messages import EnemyActions, SleepReason

@dataclass
class SleepResult:
    success: bool
    reason: SleepReason



# Enemy Class
@dataclass
class Enemy:
    name: str
    strength: int
    agility: int
    base_hp: List[int]
    dodge: int
    sleep_resist: int = 0
    stopspell_resist: int = 15
    hurt_resist: int = 0
    pattern: List[dict] = field(default_factory=lambda: [{'id': EnemyActions.ATTACK, 'weight': 100}])
    run: int = 0
    void_critical_hit: bool = False
    combat_engine: CombatEngine
    

    def __post_init__(self):
        self.max_hp = Randomizer.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0  # was e_sleep
        self.enemy_spell_stopped = False  # was e_stop
        # print(f"DEBUG: Enemy {self.name} initialized with current_hp={self.current_hp}")

    @classmethod
    def create_dummy(cls, combat_engine):
        """Creates a dummy enemy with neutral stats"""
        return cls(name="Dummy", strength=0, agility=0, base_hp=[1, 1], sleep_resist=0,
                   stopspell_resist=0, hurt_resist=0, dodge=0, pattern=[], run=0, combat_engine=combat_engine)

    def perform_enemy_action(self, player):
        action_methods = {
            EnemyActions.ATTACK: lambda: self.attack(player),
            EnemyActions.HURT: lambda: self.casts_hurt(False, player),
            EnemyActions.HURTMORE: lambda: self.casts_hurt(True, player),
            EnemyActions.HEAL: lambda: self.casts_heal(False),
            EnemyActions.HEALMORE: lambda: self.casts_heal(True),
            EnemyActions.SLEEP: lambda: self.casts_sleep(player),
            EnemyActions.STOPSPELL: lambda: self.casts_stopspell(player),
            EnemyActions.FIRE: lambda: self.breathes_fire(False, player),
            EnemyActions.STRONGFIRE: lambda: self.breathes_fire(True, player)
        }

        chosen_action = self.choose_enemy_action(player)
        action = action_methods.get(chosen_action, self.handle_unknown_action)
        result = action()
        return (chosen_action, result)

    def handle_unknown_action(self):
        """ Handles unknown enemy actions """
        raise NotImplementedError("Enemy tried to attack with something not programmed yet!!")

    def choose_enemy_action(self, player): 
        choice = None
        for item in self.pattern:
            chance = item["weight"]
            if random.randint(1, 100) <= chance:
                action = item["id"]
                if action in [EnemyActions.ATTACK, EnemyActions.HURT, EnemyActions.FIRE, EnemyActions.HURTMORE, EnemyActions.STRONGFIRE]:
                    choice = action
                    break
                if action in [EnemyActions.HEAL, EnemyActions.HEALMORE] and self.trigger_healing(): # Won't always heal
                    choice = action
                    break
                if action == EnemyActions.SLEEP and not player.is_asleep: # Don't cast sleep if player is asleep. Smart monsters.
                    choice = action
                    break
                if action == EnemyActions.STOPSPELL and not player.is_spellstopped: # Don't cast spellstop if player is stopped. Smart monsters.
                    choice = action
                    break
        return choice or EnemyActions.ATTACK
    
    def attack(self, player):
        """Enemy attacks normally"""
        enemy_damage_dealt = self.attack_damage_dealt(player.defense())
        player.current_hp -= enemy_damage_dealt
        return enemy_damage_dealt

    def casts_hurt(self, more, player):
        """ Enemy handling of hurt and hurtmore"""        
        hurt_high = [3, 10]
        hurt_low = [2, 6]
        hurtmore_high = [30, 45]
        hurtmore_low = [20, 30]
        player_mag_def = player.reduce_hurt_damage
        hurt_dmg = 0
        
        if self.enemy_spell_stopped is True:
            return "enemy_spellstopped"

        if player_mag_def and more:
            hurt_dmg = random.randint(hurtmore_low[0], hurtmore_low[1])
        elif player_mag_def and not more:
            hurt_dmg = random.randint(hurt_low[0], hurt_low[1])
        elif more:
            hurt_dmg = random.randint(hurtmore_high[0], hurtmore_high[1])
        else:
            hurt_dmg = random.randint(hurt_high[0], hurt_high[1])

        player.current_hp -= hurt_dmg
        return hurt_dmg
        
    def breathes_fire(self, more, player):
        fire_high = [16, 23]
        fire_low = [10, 14]
        strongfire_high = [65, 72]
        strongfire_low = [42, 48]
        fire_def = player.reduce_fire_damage
        fire_dmg = 0

        if fire_def and more:
            fire_dmg = random.randint(strongfire_low[0], strongfire_low[1])
        elif fire_def and not more:
            fire_dmg = random.randint(fire_low[0], fire_low[1])
        elif more:
            fire_dmg = random.randint(strongfire_high[0], strongfire_high[1])
        else:
            fire_dmg = random.randint(fire_high[0], fire_high[1])

        player.current_hp -= fire_dmg
        return fire_dmg

    def attack_damage_dealt(self, hero_defense):
        """ Enemy makes a successful attack. Returns a damage amount. """
        if hero_defense > self.strength:
            damage_range = self.weak_damage_range(self.strength)
        else:
            damage_range = self.normal_damage_range(self.strength, hero_defense)

        return Randomizer.randint(*damage_range)

    def casts_heal(self, more):
        if self.enemy_spell_stopped is True:
            return "enemy_spellstopped"
        
        heal_range = [20, 27]
        healmore_range = [85, 100]
        heal_max = self.max_hp - self.current_hp

        heal_rand = random.randint(healmore_range[0], healmore_range[1]) if more else random.randint(heal_range[0],
                                                                                                     heal_range[1])

        heal_amt = heal_rand if heal_rand < heal_max else heal_max

        self.current_hp += heal_amt
        return heal_amt

    

    def set_sleep(self, amount):
        self.enemy_sleep_count = amount
    
    def casts_sleep(self, player):
        # Sleep always hits player
        player.is_asleep = True
        return "player_now_asleep"

    def casts_stopspell(self, player):
        # 50% chance
        if random.randint(1,2) == 2:
            player.is_spellstopped = True
            return True
        else:
            return False

    def reset_battle_state(self):
        """Resets the enemy's mutable state back to default for a new battle."""
        self.max_hp = Randomizer.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0
        self.enemy_spell_stopped = False

    def did_dodge(self):
        """ Returns True if the enemy dodges """
        return Randomizer.randint(1, 64) <= self.dodge

    def is_defeated(self):
        """ Returns True if the enemy is defeated """
        return self.current_hp <= 0

    def is_asleep(self):
        if self.enemy_sleep_count <= 0:
            return SleepResult(success=False, reason=SleepReason.NOT_ASLEEP)
        if self.enemy_sleep_count == 2:
            self.enemy_sleep_count -= 1
            return SleepResult(success=True, reason=SleepReason.FIRST_ROUND_ENEMY_ASLEEP)
        self.check_for_wake_up()        

    def check_for_wake_up(self):
        """ Determines if the enemy wakes up or not """
        if self.combat_engine.enemy_wakes_up():
            self.enemy_sleep_count = 0
            return SleepResult(success=False, reason=SleepReason.ENEMY_WAKES_UP)
        else:
            return SleepResult(success=True, reason=SleepReason.ENEMY_ASLEEP)

    def does_flee(self, player_strength):
        return self.combat_engine.enemy_flees(self.strength, player_strength)
    
    def trigger_healing(self):
        return self.current_hp / self.max_hp < 0.25

    

    def take_damage(self, damage):
        self.current_hp -= damage

    @staticmethod
    def weak_damage_range(x):
        """ Returns a damage tuple for a weak attack. """
        return 0, ((x + 4) // 6)

    @staticmethod
    def normal_damage_range(x, y):
        """ Returns a damage tuple for a strong attack. """
        return ((x - y // 2) // 4), ((x - y // 2) // 2)


# Create enemy objects
enemy_instances = {k: Enemy(**v) for k, v in enemy_dict.items()}

# Create enemy names
enemy_names = [enemy.name for enemy in enemy_instances.values()]


def enemy_dummy_factory(combat_engine):
    return Enemy.create_dummy(combat_engine)
