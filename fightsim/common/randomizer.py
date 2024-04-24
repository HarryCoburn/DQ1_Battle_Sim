import random


class Randomizer:
    @staticmethod
    def randint(low, high):
        """Return a random integer N such that low <= N <= high."""
        return random.randint(low, high)

    @staticmethod
    def chance(success_rate):
        """Determine if an event with a given success rate occurs."""
        return random.random() < success_rate

    @staticmethod
    def choice(sequence):
        """Return a randomly selected element from the non-empty sequence."""
        return random.choice(sequence)

    @staticmethod
    def agility_roll(agility, surprise_factor=1):
        return agility * random.randint(1, 255) * surprise_factor
