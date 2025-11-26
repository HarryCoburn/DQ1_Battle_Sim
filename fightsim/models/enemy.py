import random
from dataclasses import dataclass, field
from typing import List
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
    combat_engine: CombatEngine
    sleep_resist: int = 0
    stopspell_resist: int = 15
    hurt_resist: int = 0
    pattern: List[dict] = field(default_factory=lambda: [{'id': EnemyActions.ATTACK, 'weight': 100}])
    run: int = 0
    void_critical_hit: bool = False
    
    

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
        enemy_actions = {
            EnemyActions.ATTACK: lambda: self.combat_engine.resolve_enemy_attack(self.strength, player.defense()),
            EnemyActions.HURT: lambda: self.combat_engine.enemy_casts_hurt(chosen_action, player.armor.reduce_hurt_damage, self.enemy_spell_stopped),
            EnemyActions.HURTMORE: lambda: self.combat_engine.enemy_casts_hurt(chosen_action, player.armor.reduce_hurt_damage, self.enemy_spell_stopped),
            EnemyActions.HEAL: lambda: self.combat_engine.enemy_casts_heal(chosen_action, self.enemy_spell_stopped, (self.max_hp - self.current_hp)),
            EnemyActions.HEALMORE: lambda: self.combat_engine.enemy_casts_heal(chosen_action, self.enemy_spell_stopped, (self.max_hp - self.current_hp)),
            EnemyActions.SLEEP: lambda: self.combat_engine.enemy_casts_sleep(chosen_action, player, self.enemy_spell_stopped),
            EnemyActions.STOPSPELL: lambda: self.combat_engine.enemy_casts_stopspell(chosen_action, player, self.enemy_spell_stopped),
            EnemyActions.FIRE: lambda: self.combat_engine.enemy_breathes_fire(chosen_action, player.armor.reduce_fire_damage),
            EnemyActions.STRONGFIRE: lambda: self.combat_engine.enemy_breathes_fire(chosen_action, player.armor.reduce_fire_damage)
        }

        chosen_action = self.choose_enemy_action(player)
        action = enemy_actions.get(chosen_action, self.handle_unknown_action)
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

    def set_sleep(self, amount):
        self.enemy_sleep_count = amount    
        
    def reset_battle_state(self):
        """Resets the enemy's mutable state back to default for a new battle."""
        self.max_hp = Randomizer.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0
        self.enemy_spell_stopped = False    

    def is_defeated(self):
        """ Returns True if the enemy is defeated """
        return self.current_hp <= 0

    def process_enemy_sleep(self):
        if self.enemy_sleep_count <= 0:
            return SleepResult(success=False, reason=SleepReason.NOT_ASLEEP)
        if self.enemy_sleep_count == 2:
            self.enemy_sleep_count -= 1
            return SleepResult(success=True, reason=SleepReason.FIRST_ROUND_ENEMY_ASLEEP)
        return self.check_for_wake_up()        

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

    def gain_hp(self, amount):
        self.current_hp += amount


# Create enemy names
enemy_names = [data['name'] for data in enemy_dict.values()]



def enemy_dummy_factory(combat_engine):
    return Enemy.create_dummy(combat_engine)


def create_enemy(enemy_key, combat_engine):
    if enemy_key not in enemy_dict:
        raise ValueError(f"Unknown enemy: {enemy_key}")
    
    enemy_data = enemy_dict[enemy_key]
    return Enemy(**enemy_data, combat_engine=combat_engine)
