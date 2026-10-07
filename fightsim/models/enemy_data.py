from fightsim.common.enemy_actions import EnemyActions

# See enemy.py for default values and what is required for a valid enemy entry.
# A pattern lists the enemy's special actions in the order they are tried; each has a
# weight% chance. If none is chosen, the enemy attacks.

# Enemies in menu order
ENEMIES = [
    {
        'name': "Slime",
        'strength': 5,
        'agility': 3,
        'base_hp': (3, 3),
        'dodge': 1
    },
    {
        'name': "Red Slime",
        'strength': 7,
        'agility': 3,
        'base_hp': (3, 3),
        'dodge': 1
    },
    {
        'name': "Drakee",
        'strength': 9,
        'agility': 6,
        'base_hp': (5, 6),
        'dodge': 1
    },
    {
        'name': "Ghost",
        'strength': 11,
        'agility': 8,
        'base_hp': (6, 7),
        'dodge': 4
    },
    {
        'name': "Magician",
        'strength': 11,
        'agility': 12,
        'base_hp': (10, 13),
        'stopspell_resist': 0,
        'dodge': 1,
        'pattern': [
            {'id': EnemyActions.HURT, 'weight': 50}
        ]
    },
    {
        'name': "Magidrakee",
        'strength': 14,
        'agility': 14,
        'base_hp': (12, 15),
        'stopspell_resist': 0,
        'dodge': 1,
        'pattern': [
            {'id': EnemyActions.HURT, 'weight': 50}
        ]
    },
    {
        'name': "Scorpion",
        'strength': 18,
        'agility': 16,
        'base_hp': (16, 20),
        'dodge': 1
    },
    {
        'name': "Druin",
        'strength': 20,
        'agility': 18,
        'base_hp': (17, 22),
        'dodge': 2
    },
    {
        'name': "Poltergeist",
        'strength': 18,
        'agility': 20,
        'base_hp': (18, 23),
        'stopspell_resist': 0,
        'dodge': 6,
        'pattern': [
            {'id': EnemyActions.HURT, 'weight': 75}
        ]
    },
    {
        'name': "Droll",
        'strength': 24,
        'agility': 24,
        'base_hp': (19, 25),
        'stopspell_resist': 14,
        'dodge': 2
    },
    {
        'name': "Drakeema",
        'strength': 22,
        'agility': 26,
        'base_hp': (16, 20),
        'sleep_resist': 2,
        'stopspell_resist': 0,
        'dodge': 6,
        'pattern': [
            {'id': EnemyActions.HEAL, 'weight': 25},
            {'id': EnemyActions.HURT, 'weight': 50}
        ]
    },
    {
        'name': "Skeleton",
        'strength': 28,
        'agility': 22,
        'base_hp': (16, 20),
        'dodge': 4
    },
    {
        'name': "Warlock",
        'strength': 28,
        'agility': 22,
        'base_hp': (23, 30),
        'sleep_resist': 3,
        'stopspell_resist': 1,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.SLEEP, 'weight': 25},
            {'id': EnemyActions.HURT, 'weight': 50}
        ]
    },
    {
        'name': "Metal Scorpion",
        'strength': 36,
        'agility': 42,
        'base_hp': (17, 22),
        'dodge': 2
    },
    {
        'name': "Wolf",
        'strength': 40,
        'agility': 30,
        'base_hp': (26, 34),
        'sleep_resist': 1,
        'dodge': 2
    },
    {
        'name': "Wraith",
        'strength': 44,
        'agility': 34,
        'base_hp': (26, 34),
        'sleep_resist': 7,
        'stopspell_resist': 0,
        'dodge': 4,
        'pattern': [
            {'id': EnemyActions.HEAL, 'weight': 25}
        ]
    },
    {
        'name': "Metal Slime",
        'strength': 10,
        'agility': 255,
        'base_hp': (4, 4),
        'sleep_resist': 15,
        'hurt_resist': 15,
        'dodge': 1,
        'pattern': [
            {'id': EnemyActions.HURT, 'weight': 75}
        ]
    },
    {
        'name': "Specter",
        'strength': 40,
        'agility': 38,
        'base_hp': (28, 36),
        'sleep_resist': 3,
        'stopspell_resist': 1,
        'dodge': 4,
        'pattern': [
            {'id': EnemyActions.SLEEP, 'weight': 25},
            {'id': EnemyActions.HURT, 'weight': 75}
        ]
    },
    {
        'name': "Wolflord",
        'strength': 50,
        'agility': 36,
        'base_hp': (29, 38),
        'sleep_resist': 4,
        'stopspell_resist': 7,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.STOPSPELL, 'weight': 50}
        ]
    },
    {
        'name': "Druinlord",
        'strength': 47,
        'agility': 40,
        'base_hp': (27, 35),
        'sleep_resist': 15,
        'stopspell_resist': 0,
        'dodge': 4,
        'pattern': [
            {'id': EnemyActions.HEAL, 'weight': 75},
            {'id': EnemyActions.HURT, 'weight': 25}
        ]
    },
    {
        'name': "Drollmagi",
        'strength': 52,
        'agility': 50,
        'base_hp': (29, 38),
        'sleep_resist': 2,
        'stopspell_resist': 2,
        'dodge': 1,
        'pattern': [
            {'id': EnemyActions.STOPSPELL, 'weight': 50}
        ],
        'run': 1
    },
    {
        'name': "Wyvern",
        'strength': 56,
        'agility': 48,
        'base_hp': (32, 42),
        'sleep_resist': 4,
        'dodge': 2,
        'run': 1
    },
    {
        'name': "Rogue Scorpion",
        'strength': 60,
        'agility': 90,
        'base_hp': (27, 35),
        'sleep_resist': 7,
        'dodge': 2,
        'run': 1
    },
    {
        'name': "Wraith Knight",
        'strength': 68,
        'agility': 56,
        'base_hp': (35, 46),
        'sleep_resist': 5,
        'stopspell_resist': 0,
        'hurt_resist': 3,
        'dodge': 4,
        'pattern': [
            {'id': EnemyActions.HEAL, 'weight': 75}
        ],
        'run': 1
    },
    {
        'name': "Golem",
        'strength': 120,
        'agility': 60,
        'base_hp': (53, 70),
        'sleep_resist': 15,
        'hurt_resist': 15,
        'dodge': 0,
        'run': 1
    },
    {
        'name': "Goldman",
        'strength': 48,
        'agility': 40,
        'base_hp': (38, 50),
        'sleep_resist': 13,
        'dodge': 1,
        'run': 1
    },
    {
        'name': "Knight",
        'strength': 76,
        'agility': 78,
        'base_hp': (42, 55),
        'sleep_resist': 6,
        'stopspell_resist': 7,
        'dodge': 1,
        'pattern': [
            {'id': EnemyActions.STOPSPELL, 'weight': 50}
        ],
        'run': 1
    },
    {
        'name': "Magiwyvern",
        'strength': 78,
        'agility': 68,
        'base_hp': (44, 58),
        'dodge': 0,
        'pattern': [
            {'id': EnemyActions.SLEEP, 'weight': 50}
        ],
        'run': 1
    },
    {
        'name': "Demon Knight",
        'strength': 79,
        'agility': 64,
        'base_hp': (38, 50),
        'sleep_resist': 15,
        'hurt_resist': 15,
        'dodge': 15,
        'run': 1
    },
    {
        'name': "Werewolf",
        'strength': 86,
        'agility': 70,
        'base_hp': (46, 60),
        'sleep_resist': 7,
        'dodge': 7,
        'run': 1
    },
    {
        'name': "Green Dragon",
        'strength': 88,
        'agility': 74,
        'base_hp': (49, 65),
        'sleep_resist': 7,
        'hurt_resist': 2,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.FIRE, 'weight': 25}
        ],
        'run': 2
    },
    {
        'name': "Starwyvern",
        'strength': 86,
        'agility': 80,
        'base_hp': (49, 65),
        'sleep_resist': 8,
        'stopspell_resist': 0,
        'hurt_resist': 1,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.HEALMORE, 'weight': 75},
            {'id': EnemyActions.FIRE, 'weight': 25}
        ],
        'run': 2
    },
    {
        'name': "Wizard",
        'strength': 80,
        'agility': 70,
        'base_hp': (49, 65),
        'sleep_resist': 17,
        'stopspell_resist': 7,
        'hurt_resist': 15,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.HURTMORE, 'weight': 50}
        ],
        'run': 2
    },
    {
        'name': "Axe Knight",
        'strength': 94,
        'agility': 82,
        'base_hp': (53, 70),
        'sleep_resist': 15,
        'stopspell_resist': 3,
        'hurt_resist': 1,
        'dodge': 1,
        'pattern': [
            {'id': EnemyActions.SLEEP, 'weight': 25}
        ],
        'run': 2
    },
    {
        'name': "Blue Dragon",
        'strength': 98,
        'agility': 84,
        'base_hp': (53, 70),
        'sleep_resist': 15,
        'hurt_resist': 7,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.FIRE, 'weight': 25}
        ],
        'run': 2
    },
    {
        'name': "Stoneman",
        'strength': 100,
        'agility': 40,
        'base_hp': (121, 160),
        'sleep_resist': 2,
        'hurt_resist': 7,
        'dodge': 1,
        'run': 3
    },
    {
        'name': "Armored Knight",
        'strength': 105,
        'agility': 86,
        'base_hp': (68, 90),
        'sleep_resist': 15,
        'stopspell_resist': 7,
        'hurt_resist': 1,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.HEALMORE, 'weight': 75},
            {'id': EnemyActions.HURTMORE, 'weight': 25}
        ],
        'run': 3
    },
    {
        'name': "Red Dragon",
        'strength': 120,
        'agility': 90,
        'base_hp': (76, 100),
        'sleep_resist': 15,
        'stopspell_resist': 7,
        'hurt_resist': 15,
        'dodge': 2,
        'pattern': [
            {'id': EnemyActions.SLEEP, 'weight': 25},
            {'id': EnemyActions.FIRE, 'weight': 25}
        ],
        'run': 3
    },
    {
        'name': "Dragonlord (first form)",
        'strength': 90,
        'agility': 75,
        'base_hp': (76, 100),
        'sleep_resist': 15,
        'hurt_resist': 15,
        'dodge': 0,
        'pattern': [
            {'id': EnemyActions.STOPSPELL, 'weight': 25},
            {'id': EnemyActions.HURTMORE, 'weight': 75}
        ],
        'run': 3,
        'void_critical_hit': True
    },
    {
        'name': "Dragonlord (second form)",
        'strength': 140,
        'agility': 200,
        'base_hp': (130, 130),
        'sleep_resist': 15,
        'hurt_resist': 15,
        'dodge': 0,
        'pattern': [
            {'id': EnemyActions.STRONGFIRE, 'weight': 50}
        ],
        'run': 3,
        "void_critical_hit": True
    }
]
