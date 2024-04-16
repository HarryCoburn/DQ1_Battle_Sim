import random
from .enemy_data import enemy_dict


# Enemy Class
class Enemy:
    def __init__(self, name, strength, agility, hp, sleep_resist, stopspell_resist,
                 hurt_resist, dodge, pattern, run, void_critical_hit=False):
        # Immutable attributes
        self.name = name  # Enemy Name
        self.strength = strength  # Enemy Strength
        self.agility = agility  # Enemy Agility
        self.base_hp = hp if isinstance(hp, list) else [hp, hp]
        self.sleep_resist = sleep_resist  # Enemy Sleep Resistance
        self.stopspell_resist = stopspell_resist  # Enemy Stopspell Resistance
        self.hurt_resist = hurt_resist  # Enemy Hurt Resistance
        self.dodge_chance = dodge  # Enemy Dodge Chance
        self.pattern = pattern  # Enemy Attack Patterns
        self.run = run  # Enemy Run Chance
        self.void_critical_hit = void_critical_hit  # Player cannot do a critical hit if true
        self.model = None

        # Mutable State         
        self.max_hp = random.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0  # was e_sleep
        self.enemy_spell_stopped = False  # was e_stop

    def __repr__(self):
        return f"Enemy(name={self.name}, strength={self.strength}, agility={self.agility}, base_hp={self.base_hp}, " \
               f"sleepR={self.sleep_resist}, stopR={self.stopspell_resist}, hurtR={self.hurt_resist}, " \
               f"dodge={self.dodge_chance}, pattern={self.pattern}, run={self.run}, voidCrit={self.void_critical_hit}, " \
               f"max_hp={self.max_hp}, current_hp={self.current_hp}, sleepCount={self.enemy_sleep_count}, " \
               f"spellStopped={self.enemy_spell_stopped})"

    def set_model(self, model):
        self.model = model  # Method to inject the model dependency

    def reset_battle_state(self):
        """Resets the enemy's mutable state back to default for a new battle."""
        self.max_hp = random.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0
        self.enemy_spell_stopped = False

    def did_dodge(self):
        return random.randint(1, 64) <= self.dodge_chance

    def is_defeated(self):
        return self.current_hp <= 0

    def is_asleep(self):
        """ Handles the sleep logic when player puts the enemy to sleep"""
        if self.enemy_sleep_count == 2:
            self.enemy_sleep_count -= 1
            self.model.text(f"The {self.name} is asleep")
        else:
            if random.randint(1, 3) == 3:
                self.model.text(f"The {self.name} woke up!")
                self.enemy_sleep_count = 0
                return False
            else:
                self.model.text(f"The {self.name} is still asleep...")
                return True

    def attack(self, hero_defense):

        if hero_defense > self.strength:
            low, high = self.weak_damage_range(self.strength)
        else:
            low, high = self.normal_damage_range(self.strength, hero_defense)

        return random.randint(low, high)

    def weak_damage_range(self, x):
        return 0, ((x + 4) // 6)

    def normal_damage_range(self, x, y):
        return ((x - y // 2) // 4), ((x - y // 2) // 2)


# Create enemy objects
enemy_instances = {k: Enemy(**v) for k, v in enemy_dict.items()}

# Create enemy names
enemy_names = [enemy.name for enemy in enemy_instances.values()]
