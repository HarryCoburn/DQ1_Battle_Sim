"""
player_leveling.py - Player stats by level, adjusted by the name formula.
"""
# Base stats for each level: strength, agility, max HP, max MP. Row 0 is level 1.
LEVEL_STATS: tuple[tuple[int, int, int, int], ...] = (
    (4, 4, 15, 0),
    (5, 4, 22, 0),
    (7, 6, 24, 5),
    (7, 8, 31, 16),
    (12, 10, 35, 20),
    (16, 10, 38, 24),
    (18, 17, 40, 26),
    (22, 20, 46, 29),
    (30, 22, 50, 36),
    (35, 31, 54, 40),
    (40, 35, 62, 50),
    (48, 40, 63, 58),
    (52, 48, 70, 64),
    (60, 55, 78, 70),
    (68, 64, 86, 72),
    (72, 70, 92, 95),
    (72, 78, 100, 100),
    (85, 84, 115, 108),
    (87, 86, 130, 115),
    (92, 88, 138, 128),
    (95, 90, 149, 135),
    (97, 90, 158, 146),
    (99, 94, 165, 153),
    (103, 98, 170, 161),
    (113, 100, 174, 161),
    (117, 105, 180, 168),
    (125, 107, 189, 175),
    (130, 115, 195, 180),
    (135, 120, 200, 190),
    (140, 130, 210, 200),
)

MIN_LEVEL: int = 1
MAX_LEVEL: int = len(LEVEL_STATS)


# Letter values for the name formula: a letter is worth the index of the group it is in.
# Characters in no group are worth 0.
LETTER_GROUPS: tuple[str, ...] = (
    "gwM", "hxN", "iyO", "jzP", "kAQ", "lBR", "mCS", "nDT", "oEU", "pFV", "aqGW",
    "brHX", "csIY", "dtJZ", "euK", "fvL",
)


def letter_value(letter: str) -> int:
    for index, group in enumerate(LETTER_GROUPS):
        if letter in group:
            return index
    return 0


def progress_mods(name: str) -> tuple[int, int]:
    """Returns name_sum from the first four letters, and the progression path (0-3) it selects."""
    name_sum = sum(map(letter_value, name[:4]))
    return name_sum, name_sum % 4


def slow_progression(name_sum: int, stat: int) -> int:
    """A stat on the slower track: 90% of its base, plus a bonus of 0-3 from the name."""
    return stat * 9 // 10 + (name_sum // 4) % 4


def adjust_stats(level: int, name: str) -> tuple[int, int, int, int]:
    """
    Returns strength, agility, max HP and max MP for a level and name.
    The name's progression path picks which two stats grow on the slower track.
    """
    strength, agility, max_hp, max_mp = LEVEL_STATS[level - 1]
    name_sum, progression = progress_mods(name)
    if progression == 0:
        strength, agility = slow_progression(name_sum, strength), slow_progression(name_sum, agility)
    elif progression == 1:
        agility, max_mp = slow_progression(name_sum, agility), slow_progression(name_sum, max_mp)
    elif progression == 2:
        strength, max_hp = slow_progression(name_sum, strength), slow_progression(name_sum, max_hp)
    else:
        max_hp, max_mp = slow_progression(name_sum, max_hp), slow_progression(name_sum, max_mp)
    return strength, agility, max_hp, max_mp
