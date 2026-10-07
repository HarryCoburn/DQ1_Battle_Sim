"""
battle.py - Battle code for DQ1 sim. Holds both player and enemy code.
"""
import random
from collections.abc import Callable
from typing import NamedTuple


from fightsim.common.enemy_actions import EnemyActions
from fightsim.common.spells import Spell
from fightsim.models.player import CRIT_CHANCE

class EnemyDamage(NamedTuple):
    normal: tuple[int,int]
    reduced: tuple[int,int]
    is_breath: bool
    verb: str


HERB_HEAL = (23,30)
RUN_MODIFIERS = (0.25, 0.375, 0.75, 1)

SPELL_COST = {
    Spell.HEAL: 4,
    Spell.HURT: 2,
    Spell.SLEEP: 2,
    Spell.STOPSPELL: 2,
    Spell.HEALMORE: 10,
    Spell.HURTMORE: 5,
}

PLAYER_HEAL = {
    Spell.HEAL: (10, 17),
    Spell.HEALMORE: (85, 100),
}

PLAYER_HURT = {
    Spell.HURT: (5, 12),
    Spell.HURTMORE: (58, 65),
}

ENEMY_HEAL = {
    EnemyActions.HEAL: (20, 27),
    EnemyActions.HEALMORE: (85, 100),
}

# Breath attacks ignore Stopspell; spells are blocked by it.
ENEMY_DAMAGE = {
    EnemyActions.HURT: EnemyDamage((3, 10), (2, 6), False, "casts Hurt"),
    EnemyActions.HURTMORE: EnemyDamage((30, 45), (20, 30), False, "casts Hurtmore"),
    EnemyActions.FIRE: EnemyDamage((16, 23), (10, 14), True, "breathes fire"),
    EnemyActions.STRONGFIRE: EnemyDamage((65, 72), (42, 48), True, "breathes strong flames at you!"),
}



class Battle:
    """
    Main battle controller
    """

    def __init__(self, player, enemy, log: Callable[[str], None], rng: random.Random, on_end: Callable[[], None]) -> None:

        self.player = player
        self.enemy = enemy
        self.rng = rng
        self.log = log
        self.on_end = on_end
        self.over = False

    # Core Fight Routines

    def start_fight(self):
        """Starts the battle loop"""
        self.enemy.max_hp = self.rng.randint(*self.enemy.base_hp)
        self.enemy.current_hp = self.enemy.max_hp
        self.log(f"You are fighting the {self.enemy.name}!")

        if self.does_enemy_surprise():
            self.log(f"The {self.enemy.name} surprises you!")
            self.advance()
        # Now we wait for the UI to call take_turn

    def take_turn(self, action: Callable[[], bool]) -> None:
        if self.over or not action():
            return
        self.advance()

    def advance(self) -> None:
        """Resolve everything until the player needs to choose again."""
        while not self.over:
            if self.enemy.is_defeated():
                self.log(f"You have defeated the {self.enemy.name}!")
                return self.finish()
            self.log("\nEnemy turn")
            self.enemy_turn()
            if self.over:
                return
            if self.player.is_defeated():
                self.log(f"You have been defeated by the {self.enemy.name}!")
                return self.finish()
            if not self.player_sleeps_through():
                return


    def finish(self) -> None:
        self.over = True
        self.on_end()

    def does_enemy_surprise(self):
        """ Determine if the enemy surprises the player based on agility and randomness. """
        player_roll = self.player.agility * self.rng.randint(0,254)
        enemy_roll = self.enemy.agility * self.rng.randint(0,254) * 0.25
        return player_roll < enemy_roll

    def resist(self, chance: int) -> bool:
        return self.rng.randint(1, 16) <= chance


    # Player Actions

    # Player Attack

    def player_sleeps_through(self) -> bool:
        if not self.player.is_asleep:
            return False
        self.player.advance_sleep()
        if self.rng.randint(1,2) == 2 or not self.player.is_asleep:
            self.player.wake()
            self.log("You wake up!")
            return False
        self.log("You're still asleep...")
        return True

    def did_player_critical_hit(self):
        return self.rng.randint(1, CRIT_CHANCE) == 1 and self.enemy.void_critical_hit is False

    def roll_player_damage(self, critical_hit: bool) -> int:
        attack = self.player.attack_num()
        if critical_hit:
            low, high = self.player.crit_range(attack)
        else:
            low, high = self.player.damage_range(attack, self.enemy.agility)
        return self.rng.randint(low,high)

    def player_attack(self) -> bool:
        crit = self.did_player_critical_hit()
        dodge = self.enemy_did_dodge()
        damage = self.roll_player_damage(crit)
        if crit:
            self.log("\nYou attack with an excellent attack!!")
        else:
            self.log("\nYou attack!")

        if dodge and not crit:
            self.log(f"But the {self.enemy.name} dodged your attack!")
        else:
            self.enemy.take_damage(damage)
            self.log(f"You hit the {self.enemy.name} for {damage} points of damage!")
        return True

    # Player uses an herb
    def use_herb(self) -> bool:
        """ Handle herb consumption by the player """
        if self.player.herb_count <= 0:
            self.log("You have no herbs!")
            return False

        self.player.consume_herb()
        if self.player.current_hp >= self.player.max_hp:
            self.log("You eat a herb, but your hit points are already at maximum!")
            return True

        healed = self.player.heal(self.rng.randint(*HERB_HEAL))
        self.log(f"You eat a herb and regain {healed} hit points!")
        return True


    # Player Flees

    def is_flee_successful(self):
        """ Return True if the player flees successfully """
        player_roll = self.player.agility * self.rng.randint(0, 254)
        enemy_roll = self.enemy.agility * self.rng.randint(0, 254) * RUN_MODIFIERS[self.enemy.run]
        return player_roll > enemy_roll

    def player_flees(self) -> bool:
        """Player attempts to flee battle."""
        self.log("You attempt to run away...")
        if self.is_flee_successful():
            self.log("You successfully flee!")
            self.finish()
        else:
            self.log(f"...but the {self.enemy.name} blocks you from running away!")
        return True

    # Player Magic

    def player_cast_magic(self, spell: Spell) -> bool:
        cost = SPELL_COST[spell]


        if self.player.current_mp < cost:
            self.log(f"Player tries to cast {spell}, but doesn't have enough MP!")
            return True # Intended. Casting without enough MP wastes turn.

        self.player.consume_mp(cost)
        if self.player.is_spellstopped:
            self.log(f"Player casts {spell}, but their magic has been sealed!")
            return True

        match spell:
            case Spell.HEAL | Spell.HEALMORE:
                self.player_heal(spell)
            case Spell.HURT | Spell.HURTMORE:
                self.player_hurt(spell)
            case Spell.SLEEP:
                self.player_casts_sleep()
            case Spell.STOPSPELL:
                self.player_casts_stopspell()
            case _:
                raise ValueError(f"No battle effect defined for spell {spell!r}")
        return True


    def player_heal(self, spell: Spell):
        healed = self.player.heal(self.rng.randint(*PLAYER_HEAL[spell]))
        if healed == 0:
            self.log(f"Player casts {spell}, but their hit points were already at maximum!")
        else:
            self.log(f"Player casts {spell}! Player is healed {healed} hit points!")

    def player_hurt(self, spell: Spell):
        damage = self.rng.randint(*PLAYER_HURT[spell])

        if self.resist(self.enemy.hurt_resist):
            self.log(f"Player casts {spell}, but the enemy resisted!")
        else:
            self.enemy.take_damage(damage)
            self.log(f"Player casts {spell}! {self.enemy.name} is hurt by {damage} hit points!")


    def player_casts_sleep(self):
        """ Player tries to cast Sleep on the enemy"""
        if self.enemy.is_asleep:
            self.log(f"Player casts Sleep! But the {self.enemy.name} is already asleep!")
        elif self.resist(self.enemy.sleep_resist):
            self.log(f"Player casts Sleep! But the {self.enemy.name} resisted!")
        else:
            self.log(f"Player casts Sleep! The {self.enemy.name} is now asleep!")
            self.enemy.fall_asleep()

    def player_casts_stopspell(self):
        """ Player tries to cast Stopspell on the enemy"""
        if self.enemy.is_spellstopped:
            self.log(f"Player casts Stopspell! But the {self.enemy.name}'s magic was already blocked!")
        elif self.resist(self.enemy.stopspell_resist):
            self.log(f"Player casts Stopspell! But the {self.enemy.name} resisted!")
        else:
            self.log(f"Player casts Stopspell! The {self.enemy.name}'s magic is now blocked!!")
            self.enemy.is_spellstopped = True


    # Enemy Actions
    #
    def enemy_turn(self):
        """ Handles the Enemy's turn """

        if self.enemy.is_asleep:
            self.process_enemy_sleep()
        elif self.should_enemy_flee():
            self.enemy_flees()
        else:
            self.perform_enemy_action()

    def enemy_did_dodge(self):
        return self.rng.randint(1,64) <= self.enemy.dodge

    def process_enemy_sleep(self)-> None:
        self.enemy.advance_sleep()
        if self.enemy.is_asleep:
            self.log(f"The {self.enemy.name} is asleep")
        elif self.rng.randint(1,3) == 3:
            self.enemy.wake()
            self.log(f"The {self.enemy.name} woke up!")
        else:
            self.log(f"The {self.enemy.name} is still asleep...")
            self.enemy.stay_asleep()

    def should_enemy_flee(self):
        return self.player.strength > self.enemy.strength * 2 and self.rng.randint(1, 4) == 4

    def enemy_flees(self):
        """ Enemy runs away. End the combat"""
        self.log(f"The {self.enemy.name} flees from your superior strength!")
        self.finish()

    def enemy_can_use(self, action: EnemyActions) -> bool:
        """Skip actions that would be pointless right now."""
        match action:
            case EnemyActions.HEAL | EnemyActions.HEALMORE:
                return self.enemy.trigger_healing()
            case EnemyActions.SLEEP:
                return not self.player.is_asleep
            case EnemyActions.STOPSPELL:
                return not self.player.is_spellstopped
            case _:
                return True

    def enemy_choose_attack(self) -> EnemyActions:
        for item in self.enemy.pattern:
            if self.rng.randint(1, 100) <= item["weight"] and self.enemy_can_use(item["id"]):
                return item["id"]
        return EnemyActions.ATTACK

    def perform_enemy_action(self) -> None:
        action = self.enemy_choose_attack()
        match action:
            case EnemyActions.ATTACK:
                self.enemy_attack()
            case EnemyActions.HEAL | EnemyActions.HEALMORE:
                self.enemy_casts_heal(action)
            case EnemyActions.SLEEP:
                self.enemy_casts_sleep()
            case EnemyActions.STOPSPELL:
                self.enemy_casts_stopspell()
            case _ if action in ENEMY_DAMAGE:
                self.enemy_deals_damage(action)
            case _:
                raise NotImplementedError(f"No battle effect defined for enemy action {action!r}")

    def enemy_spell_blocked(self, verb: str) -> bool:
        """Log and return True if the enemy's magic is sealed."""
        if self.enemy.is_spellstopped:
            self.log(f"The {self.enemy.name} {verb}, but their spell has been blocked!")
            return True
        return False

    def enemy_attack(self) -> None:
        damage = self.rng.randint(*self.enemy.attack_range(self.player.defense()))
        self.player.take_damage(damage)
        self.log(f"The {self.enemy.name} attacks! You are hit for {damage} damage.")

    def enemy_deals_damage(self, action: EnemyActions) -> None:
        """Hurt, Hurtmore and the breath attacks."""
        attack = ENEMY_DAMAGE[action]
        if not attack.is_breath and self.enemy_spell_blocked(attack.verb):
            return

        protected = self.player.reduce_fire_damage if attack.is_breath else self.player.reduce_hurt_damage
        damage = self.rng.randint(*(attack.reduced if protected else attack.normal))
        self.player.take_damage(damage)
        self.log(f"The {self.enemy.name} {attack.verb}! You are hurt for {damage} damage!")

    def enemy_casts_heal(self, action: EnemyActions) -> None:
        verb = f"casts {action.name.title()}"
        if self.enemy_spell_blocked(verb):
            return

        healed = self.enemy.heal(self.rng.randint(*ENEMY_HEAL[action]))
        if healed == 0:
            self.log(f"The {self.enemy.name} {verb}, but its hit points were already at maximum!")
        else:
            self.log(f"The {self.enemy.name} {verb}! The {self.enemy.name} regains {healed} hit points!")

    def enemy_casts_sleep(self) -> None:
        if self.enemy_spell_blocked("casts Sleep"):
            return
        self.player.fall_asleep()
        self.log(f"The {self.enemy.name} casts Sleep. You fall asleep!!")

    def enemy_casts_stopspell(self) -> None:
        """50% chance of failure."""
        if self.enemy_spell_blocked("casts Stopspell"):
            return
        if self.rng.randint(1, 2) == 2:
            self.player.is_spellstopped = True
            self.log(f"The {self.enemy.name} casts Stopspell! Your magic has been blocked!")
        else:
            self.log(f"The {self.enemy.name} casts Stopspell, but the spell fails!")
