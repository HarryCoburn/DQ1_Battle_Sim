from enum import Enum, auto
import random

# Enemy Class
class Enemy:
    def __init__(self, name, strength, agility, hp, sleepR, stopR, hurtR, dodge, pattern, run, voidCrit = False):
        # Immutable attributes
        self.name = name # Enemy Name
        self.strength = strength # Enemy Strength
        self.agility = agility # Enemy Agility
        self.base_hp = hp if isinstance(hp, list) else [hp, hp]        
        self.sleepR = sleepR # Enemy Sleep Resistance
        self.stopR = stopR # Enemy Stopspell Resistance
        self.hurtR = hurtR # Enemy Hurt Resistance
        self.dodge = dodge # Enemy Dodge Chance
        self.pattern = pattern # Enemy Attack Patterns
        self.run = run # Enemy Run Chance
        self.voidCrit = voidCrit # Player cannot do a critical hit if true

        # Mutable State         
        self.max_hp = random.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.sleepCount = 0 # was e_sleep
        self.spellStopped = False # was e_stop

    def __repr__(self):
        return f"Enemy(name={self.name}, strength={self.strength}, agility={self.agility}, base_hp={self.base_hp}, sleepR={self.sleepR}, stopR={self.stopR}, hurtR={self.hurtR}, dodge={self.dodge}, pattern={self.pattern}, run={self.run}, voidCrit={self.voidCrit}, max_hp={self.max_hp}, current_hp={self.current_hp}, sleepCount={self.sleepCount}, spellStopped={self.spellStopped})"
      
    def reset_battle_state(self):
        """Resets the enemy's mutable state back to default for a new battle."""
        self.max_hp = random.randint(self.base_hp[0], self.base_hp[1])
        self.current_hp = self.max_hp
        self.e_sleep = 0
        self.e_stop = False

# Enemy Actions
class Action(Enum):
   ATTACK = auto()
   HEAL = auto()
   HURT = auto()
   SLEEP = auto()
   STOPSPELL = auto()
   FIRE = auto()
   HEALMORE = auto()
   HURTMORE = auto()
   STRONGFIRE = auto()


# Enemy Dictionary   
enemy_dict = {
    'slime': {
        'name': "Slime",
        'strength': 5,
        'agility': 3,
        'hp': 3,
        'sleepR': 0,
        'stopR': 15,
        'hurtR': 0,
        'dodge': 1,        
        'pattern': [{
            'id': Action.ATTACK,
            'weight': 100
            }],
        'run': 0,
      },
    'rslime': {
        'name': "Red Slime",
        'strength': 7,
        'agility': 3,
        'hp': 3,
        'sleepR': 0,
        'stopR': 15,
        'hurtR': 0,
        'dodge': 1,
        'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
        'run': 0
  },
  'drakee': {
    'name': "Drakee",
    'strength': 9,
    'agility': 6,
    'hp': [5, 6],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "ghost": {
    'name': "Ghost",
    'strength': 11,
    'agility': 8,
    'hp': [6, 7],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 4,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "magician": {
    'name': "Magician",
    'strength': 11,
    'agility': 12,
    'hp': [10, 13],
    'sleepR': 0,
    'stopR': 0,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [
      { 'id': Action.HURT, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "magidrakee": {
    'name': "Magidrakee",
    'strength': 14,
    'agility': 14,
    'hp': [12, 15],
    'sleepR': 0,
    'stopR': 0,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [
      { 'id': Action.HURT, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "scorpion": {
    'name': "Scorpion",
    'strength': 18,
    'agility': 16,
    'hp': [16, 20],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "druin": {
    'name': "Druin",
    'strength': 20,
    'agility': 18,
    'hp': [17, 22],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "poltergeist": {
    'name': "Poltergeist",
    'strength': 18,
    'agility': 20,
    'hp': [18, 23],
    'sleepR': 0,
    'stopR': 0,
    'hurtR': 0,
    'dodge': 6,
    'pattern': [
      { 'id': Action.HURT, 'weight': 75 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "droll": {
    'name': "Droll",
    'strength': 24,
    'agility': 24,
    'hp': [19, 25],
    'sleepR': 0,
    'stopR': 14,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "drakeema": {
    'name': "Drakeema",
    'strength': 22,
    'agility': 26,
    'hp': [16, 20],
    'sleepR': 2,
    'stopR': 0,
    'hurtR': 0,
    'dodge': 6,
    'pattern': [
      { 'id': Action.HEAL, 'weight': 25 },
      { 'id': Action.HURT, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "skeleton": {
    'name': "Skeleton",
    'strength': 28,
    'agility': 22,
    'hp': [16, 20],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 4,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "warlock": {
    'name': "Warlock",
    'strength': 28,
    'agility': 22,
    'hp': [23, 30],
    'sleepR': 3,
    'stopR': 1,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [
      { 'id': Action.SLEEP, 'weight': 25 },
      { 'id': Action.HURT, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "mscorpion": {
    'name': "Metal Scorpion",
    'strength': 36,
    'agility': 42,
    'hp': [17, 22],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "wolf": {
    'name': "Wolf",
    'strength': 40,
    'agility': 30,
    'hp': [26, 34],
    'sleepR': 1,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 0
  },
  "wraith": {
    'name': "Wraith",
    'strength': 44,
    'agility': 34,
    'hp': [26, 34],
    'sleepR': 7,
    'stopR': 0,
    'hurtR': 0,
    'dodge': 4,
    'pattern': [
      { 'id': Action.HEAL, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "Metal Slime": {
    'name': "Metal Slime",
    'strength': 10,
    'agility': 255,
    'hp': 4,
    'sleepR': 15,
    'stopR': 15,
    'hurtR': 15,
    'dodge': 1,
    'pattern': [
      { 'id': Action.HURT, 'weight': 75 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "specter": {
    'name': "Specter",
    'strength': 40,
    'agility': 38,
    'hp': [28, 36],
    'sleepR': 3,
    'stopR': 1,
    'hurtR': 0,
    'dodge': 4,
    'pattern': [
      { 'id': Action.SLEEP, 'weight': 25 },
      { 'id': Action.HURT, 'weight': 75 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "wolflord": {
    'name': "Wolflord",
    'strength': 50,
    'agility': 36,
    'hp': [29, 38],
    'sleepR': 4,
    'stopR': 7,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [
      { 'id': Action.STOPSPELL, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "druinlord": {
    'name': "Druinlord",
    'strength': 47,
    'agility': 40,
    'hp': [27, 35],
    'sleepR': 15,
    'stopR': 0,
    'hurtR': 0,
    'dodge': 4,
    'pattern': [
      { 'id': Action.HEAL, 'weight': 75 },
      { 'id': Action.HURT, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 0
  },
  "drollmagi": {
    'name': "Drollmagi",
    'strength': 52,
    'agility': 50,
    'hp': [29, 38],
    'sleepR': 2,
    'stopR': 2,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [
      { 'id': Action.STOPSPELL, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 1
  },
  "wyvern": {
    'name': "Wyvern",
    'strength': 56,
    'agility': 48,
    'hp': [32, 42],
    'sleepR': 4,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 1
  },
  "rogue_scorpion": {
    'name': "Rogue Scorpion",
    'strength': 60,
    'agility': 90,
    'hp': [27, 35],
    'sleepR': 7,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 2,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 1
  },
  "w_knight": {
    'name': "Wraith Knight",
    'strength': 68,
    'agility': 56,
    'hp': [35, 46],
    'sleepR': 5,
    'stopR': 0,
    'hurtR': 3,
    'dodge': 4,
    'pattern': [
      { 'id': Action.HEAL, 'weight': 75 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 1
  },
  "golem": {
    'name': "Golem",
    'strength': 120,
    'agility': 60,
    'hp': [53, 70],
    'sleepR': 15,
    'stopR': 15,
    'hurtR': 15,
    'dodge': 0,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 1
  },
  "goldman": {
    'name': "Goldman",
    'strength': 48,
    'agility': 40,
    'hp': [38, 50],
    'sleepR': 13,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 1
  },
  "knight": {
    'name': "Knight",
    'strength': 76,
    'agility': 78,
    'hp': [42, 55],
    'sleepR': 6,
    'stopR': 7,
    'hurtR': 0,
    'dodge': 1,
    'pattern': [
      { 'id': Action.STOPSPELL, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 1
  },
  "magiwyvern": {
    'name': "Magiwyvern",
    'strength': 78,
    'agility': 68,
    'hp': [44, 58],
    'sleepR': 0,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 0,
    'pattern': [
      { 'id': Action.SLEEP, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 1
  },
  "d_knight": {
    'name': "Demon Knight",
    'strength': 79,
    'agility': 64,
    'hp': [38, 50],
    'sleepR': 15,
    'stopR': 15,
    'hurtR': 15,
    'dodge': 15,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 1
  },
  "werewolf": {
    'name': "Werewolf",
    'strength': 86,
    'agility': 70,
    'hp': [46, 60],
    'sleepR': 7,
    'stopR': 15,
    'hurtR': 0,
    'dodge': 7,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 1
  },
  "Green Dragon": {
    'name': "Green Dragon",
    'strength': 88,
    'agility': 74,
    'hp': [49, 65],
    'sleepR': 7,
    'stopR': 15,
    'hurtR': 2,
    'dodge': 2,
    'pattern': [
      { 'id': Action.FIRE, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 2
  },
  "starwyvern": {
    'name': "Starwyvern",
    'strength': 86,
    'agility': 80,
    'hp': [49, 65],
    'sleepR': 8,
    'stopR': 0,
    'hurtR': 1,
    'dodge': 2,
    'pattern': [
      { 'id': Action.HEALMORE, 'weight': 75 },
      { 'id': Action.FIRE, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 2
  },
  "wizard": {
    'name': "Wizard",
    'strength': 80,
    'agility': 70,
    'hp': [49, 65],
    'sleepR': 17,
    'stopR': 7,
    'hurtR': 15,
    'dodge': 2,
    'pattern': [
      { 'id': Action.HURTMORE, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 50 }
    ],
    'run': 2
  },
  "axe_knight": {
    'name': "Axe Knight",
    'strength': 94,
    'agility': 82,
    'hp': [53, 70],
    'sleepR': 15,
    'stopR': 3,
    'hurtR': 1,
    'dodge': 1,
    'pattern': [
      { 'id': Action.SLEEP, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 2
  },
  "blue_dragon": {
    'name': "Blue Dragon",
    'strength': 98,
    'agility': 84,
    'hp': [53, 70],
    'sleepR': 15,
    'stopR': 15,
    'hurtR': 7,
    'dodge': 2,
    'pattern': [
      { 'id': Action.FIRE, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 2
  },
  "stoneman": {
    'name': "Stoneman",
    'strength': 100,
    'agility': 40,
    'hp': [121, 160],
    'sleepR': 2,
    'stopR': 15,
    'hurtR': 7,
    'dodge': 1,
    'pattern': [{ 'id': Action.ATTACK, 'weight': 100 }],
    'run': 3
  },
  "armored_knight": {
    'name': "Armored Knight",
    'strength': 105,
    'agility': 86,
    'hp': [68, 90],
    'sleepR': 15,
    'stopR': 7,
    'hurtR': 1,
    'dodge': 2,
    'pattern': [
      { 'id': Action.HEALMORE, 'weight': 75 },
      { 'id': Action.HURTMORE, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 3
  },
  "red_dragon": {
    'name': "Red Dragon",
    'strength': 120,
    'agility': 90,
    'hp': [76, 100],
    'sleepR': 15,
    'stopR': 7,
    'hurtR': 15,
    'dodge': 2,
    'pattern': [
      { 'id': Action.SLEEP, 'weight': 25 },
      { 'id': Action.FIRE, 'weight': 25 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],
    'run': 3
  },
  "dragonlord_first": {
    'name': "Dragonlord (first form)",
    'strength': 90,
    'agility': 75,
    'hp': [76, 100],
    'sleepR': 15,
    'stopR': 15,
    'hurtR': 15,
    'dodge': 0,
    'pattern': [
      { 'id': Action.STOPSPELL, 'weight': 25 },
      { 'id': Action.HURTMORE, 'weight': 75 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],    
    'run': 3,
    'voidCrit': True
  },
  "dragonlord_second": {
    'name': "Dragonlord (second form)",
    'strength': 140,
    'agility': 200,
    'hp': 130,
    'sleepR': 15,
    'stopR': 15,
    'hurtR': 15,
    'dodge': 0,
    'pattern': [
      { 'id': Action.STRONGFIRE, 'weight': 50 },
      { 'id': Action.ATTACK, 'weight': 100 }
    ],    
    'run': 3,
    "voidCrit": True
  }
}

# Create enemy objects
enemy_instances = {k: Enemy(**v) for k, v in enemy_dict.items()}

# Create enemy names
enemy_names = [enemy.name for enemy in enemy_instances.values()]