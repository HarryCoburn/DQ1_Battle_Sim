from dataclasses import dataclass, field
from typing import List
from .enemy_data import enemy_dict

from ..common.messages import EnemyActions


# Enemy Class
@dataclass
class Enemy:
    name: str
    strength: int
    agility: int
    base_hp: List[int]
    dodge: int
    max_hp: int = 0
    current_hp: int = 0
    sleep_count: int = 0
    is_spellstopped: bool = False
    sleep_resist: int = 0
    stopspell_resist: int = 15
    hurt_resist: int = 0
    pattern: List[dict] = field(default_factory=lambda: [{'id': EnemyActions.ATTACK, 'weight': 100}])
    run: int = 0
    void_critical_hit: bool = False
    sleep_turns: int = 0

    @property
    def is_asleep(self) -> bool:
        return self.sleep_turns > 0

    def advance_sleep(self):
        self.sleep_turns -= 1

    def wake(self):
        self.sleep_turns = 0

    def stay_asleep(self):
        self.sleep_turns = 1

    def fall_asleep(self):
        self.sleep_turns = 2

    @classmethod
    def create_dummy(cls):
        """Creates a dummy enemy with neutral stats"""
        return cls(name="Dummy", strength=0, agility=0, base_hp=[1, 1], sleep_resist=0,
                   stopspell_resist=0, hurt_resist=0, dodge=0, pattern=[], run=0)

    def is_defeated(self):
        """ Returns True if the enemy is defeated """
        return self.current_hp <= 0

    def trigger_healing(self):
        return self.current_hp / self.max_hp < 0.25

    def attack_range(self, hero_defense):
        """ Enemy makes a successful attack. Returns a damage amount. """
        if hero_defense > self.strength:
            return self.weak_damage_range(self.strength)
        else:
            return self.normal_damage_range(self.strength, hero_defense)



    def take_damage(self, amount: int) -> int:
        dealt = min(amount, self.current_hp)
        self.current_hp -= dealt
        return dealt

    def heal(self, amount: int) -> int:
        healed = min(amount, self.max_hp - self.current_hp)
        self.current_hp += healed
        return healed

    @staticmethod
    def weak_damage_range(x):
        """ Returns a damage tuple for a weak attack. """
        return 0, ((x + 4) // 6)

    @staticmethod
    def normal_damage_range(x, y):
        """ Returns a damage tuple for a strong attack. """
        return ((x - y // 2) // 4), ((x - y // 2) // 2)


# Create enemy names
enemy_names = [v['name'] for v in enemy_dict.values()]


def create_enemy(name: str) -> Enemy:
    """ Builds a fresh Enemy from enemy_dict by display name. Raises KeyError if not found. """
    for key, value in enemy_dict.items():
        if value['name'] == name:
            return Enemy(**enemy_dict[key])
    raise KeyError(name)


def enemy_dummy_factory():
    return Enemy.create_dummy()
