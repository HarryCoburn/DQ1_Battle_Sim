"""
combatant.py - Hit point and sleep handling shared by the player and enemies.
"""


class Combatant:
    """
    Mixin for a fighter. The class using it provides current_hp, max_hp and sleep_turns.
    Holds no fields of its own, so it can sit under any dataclass.
    """
    current_hp: int
    max_hp: int
    sleep_turns: int

    def is_defeated(self) -> bool:
        return self.current_hp <= 0

    def take_damage(self, amount: int) -> int:
        """Lowers HP, never below 0. Returns the damage actually dealt."""
        dealt = min(amount, self.current_hp)
        self.current_hp -= dealt
        return dealt

    def heal(self, amount: int) -> int:
        """Raises HP, never above max_hp. Returns the HP actually restored."""
        healed = min(amount, self.max_hp - self.current_hp)
        self.current_hp += healed
        return healed

    @property
    def is_asleep(self) -> bool:
        return self.sleep_turns > 0

    def advance_sleep(self) -> None:
        self.sleep_turns -= 1

    def wake(self) -> None:
        self.sleep_turns = 0
