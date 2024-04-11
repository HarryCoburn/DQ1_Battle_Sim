"""
Player class
"""

from dataclasses import dataclass, field
from typing import Tuple, List
from .items import *
import math
import random

@dataclass
class Player:
    name: str = "Rollo"
    name_sum: int = 0
    progression: int = 0
    level: int = 1
    strength: int = 4
    agility: int = 4
    curr_hp: int = 15
    max_hp: int = 15
    curr_mp: int = 0
    max_mp: int = 0
    weapon: Weapon = field(default_factory=lambda: weapon_instances["unarmed"])
    armor: Armor = field(default_factory=lambda: armor_instances["naked"])
    shield: Shield = field(default_factory=lambda: shield_instances["no_shield"])
    player_magic: list = field(default_factory=list)
    herb_count: int = 0
    reduce_hurt_damage: bool = False
    reduce_fire_damage: bool = False
    print(weapon)
    attack_num: int = 0
    is_asleep: bool = False
    is_spellstopped: bool = False
    sleep_count: int = 6
    level_stats: list = field(default_factory=lambda: [
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
        ])
    model = None # Placeholder
    
    def __post_init__(self):
        self.attack_num = self.strength + self.weapon.modifier         

    # Static Classes
    @staticmethod
    def slow_prog(name_sum, stat) -> int:
        '''
        Formula for lower stats
        '''
        return math.floor(stat * (9 / 10) + (math.floor(name_sum / 4) % 4))
    
    @staticmethod
    def letter_stat(ltr):
        '''
        Calculates letter values of the name for stat calculations
        '''
        ltr_clusters = ["gwM", "hxN", "iyO", "jzP", "kAQ", "lBR", "mCS", "nDT", "oEU", "pFV", "aqGW",
        "brHX", "csIY", "dtJZ", "euK", "fvL"]
        for index, cluster in enumerate(ltr_clusters):
            if ltr in cluster:
                return index
        return 0

    def set_model(self, model):
        self.model = model # Method to inject the model dependency
    
    def progress_mods(self, name):
        '''
        Calcualte name_sum and the progression modifier
        '''
        letters = name[0:4]        
        return (sum(map(self.letter_stat, letters)), math.floor(self.name_sum % 4))
    
    def level_up(self):
        '''
        Main level up function

        The function reads the new level, recalculates the name_sum and progression path
        Then uses the right level_base to adjust the stats of the player.
        '''
        level_base = self.level_stats[int(self.level) - 1]
        self.name_sum, self.progression = self.progress_mods(self.name)
        # Four types of progression
        if self.progression == 0:
            self.strength = self.slow_prog(self.name_sum, level_base[0])
            self.agility = self.slow_prog(self.name_sum, level_base[1])
            self.max_hp = level_base[2]
            self.max_mp = level_base[3]
        elif self.progression == 1:
            self.strength = level_base[0]
            self.agility = self.slow_prog(self.name_sum, level_base[1])
            self.max_hp = level_base[2]
            self.max_mp = self.slow_prog(self.name_sum, level_base[3])
        elif self.progression == 2:
            self.strength = self.slow_prog(self.name_sum, level_base[0])
            self.agility = level_base[1]
            self.max_hp = self.slow_prog(self.name_sum, level_base[2])
            self.max_mp = level_base[3]
        else:
            self.strength = level_base[0]
            self.agility = level_base[1]
            self.max_hp = self.slow_prog(self.name_sum, level_base[2])
            self.max_mp = self.slow_prog(self.name_sum, level_base[3])
        self.curr_hp = self.max_hp
        self.curr_mp = self.max_mp
        self.build_p_magic_list()

    def build_p_magic_list(self) -> List[str]:
        '''
        Create a list of available spells based on level
        '''            
        self.player_magic = []
        if self.level >= 3:
            self.player_magic.append("Heal")
        if self.level >= 4:
            self.player_magic.append("Hurt")
        if self.level >= 7:
            self.player_magic.append("Sleep")
        if self.level >= 10:
            self.player_magic.append("Stopspell")
        if self.level >= 17:
            self.player_magic.append("Healmore")
        if self.level >= 19:
            self.player_magic.append("Hurtmore")        

    @staticmethod    
    def find_key_by_value(d, value_to_find):
        for key, value in d.items():            
            if value.name == value_to_find:
                return key
        return None

    def equip_weapon(self, weapon_name: str):
        key = self.find_key_by_value(weapon_instances, weapon_name)
        weapon_instance = weapon_instances.get(key)
        if weapon_instance:        
            self.weapon = weapon_instance
            if self.model:
                self.model.notify_weapon_change()
        else:
            print(f"Weapon {weapon_name} not found.")        
    
    def equip_armor(self, armor_name: str):
        key = self.find_key_by_value(armor_instances, armor_name)
        armor_instance = armor_instances.get(key)
        if armor_instance:
            self.armor = armor_instance
            if self.armor.reduce_hurt_damage:
                self.reduce_hurt_damage = True
            else:
                self.reduce_hurt_damage = False
            if self.armor.reduce_fire_damage:
                self.reduce_fire_damage = True
            else:
                self.reduce_fire_damage = False
            if self.model:
                self.model.notify_armor_change()
        else:
            print(f"Armor {armor_name} not found.")     

    def equip_shield(self, shield_name: str):
        key = self.find_key_by_value(shield_instances, shield_name)
        shield_instance = shield_instances.get(key)
        if shield_instance:        
            self.shield = shield_instance
            if self.model:
                self.model.notify_shield_change()
        else:
            print(f"Shield {shield_name} not found.")     

    def change_level(self, new_level: int):
        self.level = new_level
        self.level_up()
    
    def did_crit(self):
        return random.randint(1,32) == 1

    def damage_range(self,x,y):
        return (((x - y // 2) // 4), ((x - y // 2) // 2))
    
    def crit_range(self,x):
        return ((x//2), x)
    
    def handle_sleep(self):
        if self.is_asleep is False:
            return False
        self.sleep_count -= 1
        if random.randint(1,2) == 2 or self.player.sleep_count <= 0:
            self.is_asleep = False
            self.sleep_count = 6
            return False
        else:
            return True

    