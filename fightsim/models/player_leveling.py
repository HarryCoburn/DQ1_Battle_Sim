from math import floor


class _Levelling:
    """
    Controls how the player levels up and down and recalculates stats.
    """
    def __init__(self):
        # level_stats holds the base leveling data for the player
        self.level_stats = [
            [4, 4, 15, 0],
            [5, 4, 22, 0],
            [7, 6, 24, 5],
            [7, 8, 31, 16],
            [12, 10, 35, 20],
            [16, 10, 38, 24],
            [18, 17, 40, 26],
            [22, 20, 46, 29],
            [30, 22, 50, 36],
            [35, 31, 54, 40],
            [40, 35, 62, 50],
            [48, 40, 63, 58],
            [52, 48, 70, 64],
            [60, 55, 78, 70],
            [68, 64, 86, 72],
            [72, 70, 92, 95],
            [72, 78, 100, 100],
            [85, 84, 115, 108],
            [87, 86, 130, 115],
            [92, 88, 138, 128],
            [95, 90, 149, 135],
            [97, 90, 158, 146],
            [99, 94, 165, 153],
            [103, 98, 170, 161],
            [113, 100, 174, 161],
            [117, 105, 180, 168],
            [125, 107, 189, 175],
            [130, 115, 195, 180],
            [135, 120, 200, 190],
            [140, 130, 210, 200]
        ]
        self.name_sum = 0

    @staticmethod
    def calculate_slow_progression(name_sum, stat) -> int:
        """
        Formula for the slower progression of stats. Takes the name_sum and the stat base for a particular level
        and calculates the true value using this formula.
        """
        return floor(stat * (9 / 10) + (floor(name_sum / 4) % 4))

    @staticmethod
    def calculate_letter_stat(ltr):
        """
        Calculates letter values of the name for stat calculations
        """
        ltr_clusters = ["gwM", "hxN", "iyO", "jzP", "kAQ", "lBR", "mCS", "nDT", "oEU", "pFV", "aqGW",
                        "brHX", "csIY", "dtJZ", "euK", "fvL"]
        for index, cluster in enumerate(ltr_clusters):
            if ltr in cluster:
                return index
        return 0

    def progress_mods(self, name):
        """
        Calculate name_sum and progression modifier
        """
        letters = name[0:4]
        return sum(map(self.calculate_letter_stat, letters)), floor(self.name_sum % 4)

    def adjust_stats(self, level, name):
        """
        Main level up function

        The function reads the new level, recalculates the name_sum and progression path
        Then uses the right level_base to adjust the stats of the player.
        """
        level_base = self.level_stats[level - 1]
        name_sum, progression = self.progress_mods(name)
        # Four types of progression
        if progression == 0:
            strength = self.calculate_slow_progression(name_sum, level_base[0])
            agility = self.calculate_slow_progression(name_sum, level_base[1])
            max_hp = level_base[2]
            max_mp = level_base[3]
        elif progression == 1:
            strength = level_base[0]
            agility = self.calculate_slow_progression(name_sum, level_base[1])
            max_hp = level_base[2]
            max_mp = self.calculate_slow_progression(name_sum, level_base[3])
        elif progression == 2:
            strength = self.calculate_slow_progression(name_sum, level_base[0])
            agility = level_base[1]
            max_hp = self.calculate_slow_progression(name_sum, level_base[2])
            max_mp = level_base[3]
        else:
            strength = level_base[0]
            agility = level_base[1]
            max_hp = self.calculate_slow_progression(name_sum, level_base[2])
            max_mp = self.calculate_slow_progression(name_sum, level_base[3])
        return strength, agility, max_hp, max_mp

        # self.curr_hp = self.max_hp
        # self.curr_mp = self.max_mp
        # self.build_p_magic_list()