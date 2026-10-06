from dataclasses import dataclass, field
from typing import List, Optional
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
    enemy_sleep_count: int = 0
    enemy_spell_Stopped: bool = False
    sleep_resist: int = 0
    stopspell_resist: int = 15
    hurt_resist: int = 0
    pattern: List[dict] = field(default_factory=lambda: [{'id': EnemyActions.ATTACK, 'weight': 100}])
    run: int = 0
    void_critical_hit: bool = False
    model: Optional[any] = None

    @classmethod
    def create_dummy(cls):
        """Creates a dummy enemy with neutral stats"""
        return cls(name="Dummy", strength=0, agility=0, base_hp=[1, 1], sleep_resist=0,
                   stopspell_resist=0, hurt_resist=0, dodge=0, pattern=[], run=0)

    def is_spell_stopped(self, spell_name):
        if self.enemy_spell_stopped:
            self.model.text(f"""The {self.model.enemy["name"]} casts {spell_name}, but their spell has been blocked!""")
            return True
        return False

    def set_model(self, model):
        self.model = model  # Method to inject the model dependency

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


def enemy_dummy_factory():
    return Enemy.create_dummy()
