import random
import enemy_data


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
        self.dodge = dodge  # Enemy Dodge Chance
        self.pattern = pattern  # Enemy Attack Patterns
        self.run = run  # Enemy Run Chance
        self.void_critical_hit = void_critical_hit  # Player cannot do a critical hit if true

        # Mutable State         
        self.max_hp = random.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0  # was e_sleep
        self.enemy_spell_stopped = False  # was e_stop

    def __repr__(self):
        return f"Enemy(name={self.name}, strength={self.strength}, agility={self.agility}, base_hp={self.base_hp}, " \
               f"sleepR={self.sleep_resist}, stopR={self.stopspell_resist}, hurtR={self.hurt_resist}, " \
               f"dodge={self.dodge}, pattern={self.pattern}, run={self.run}, voidCrit={self.void_critical_hit}, " \
               f"max_hp={self.max_hp}, current_hp={self.current_hp}, sleepCount={self.enemy_sleep_count}, " \
               f"spellStopped={self.enemy_spell_stopped})"

    def reset_battle_state(self):
        """Resets the enemy's mutable state back to default for a new battle."""
        self.max_hp = random.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.enemy_sleep_count = 0
        self.enemy_spell_stopped = False


# Create enemy objects
enemy_instances = {k: Enemy(**v) for k, v in enemy_data.enemy_dict.items()}

# Create enemy names
enemy_names = [enemy.name for enemy in enemy_instances.values()]
