from dataclasses import dataclass, field
from typing import List, Optional
from .enemy_data import enemy_dict
from ..common.randomizer import Randomizer
from ..common.messages import EnemyActions


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
    model: Optional[any] = None

    def __post_init__(self):
        self.max_hp = Randomizer.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0  # was e_sleep
        self.enemy_spell_stopped = False  # was e_stop

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
        """
        Check and update the sleep status of the enemy.
        Returns True if the enemy remains asleep, otherwise False.
        """
        if self.enemy_sleep_count == 2:
            self.enemy_sleep_count -= 1
            self.model.text(f"The {self.name} is asleep")
            return True
        else:
            return self.update_sleep_status()

    def update_sleep_status(self):
        """ Determines if the enemy wakes up or not """
        if Randomizer.randint(1, 3) == 3:
            return self.wake_up()
        else:
            return self.remain_asleep()

    def wake_up(self):
        """ Wakes up the enemy """
        self.model.text(f"The {self.name} woke up!")
        self.enemy_sleep_count = 0
        return False

    def remain_asleep(self):
        """ The enemy remains asleep """
        self.model.text(f"The {self.name} is still asleep...")
        return True

    def trigger_healing(self):
        return self.current_hp / self.max_hp < 0.25

    def attack(self, hero_defense):
        """ Enemy makes a successful attack. Returns a damage amount. """
        if hero_defense > self.strength:
            damage_range = self.weak_damage_range(self.strength)
        else:
            damage_range = self.normal_damage_range(self.strength, hero_defense)

        return Randomizer.randint(*damage_range)

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
