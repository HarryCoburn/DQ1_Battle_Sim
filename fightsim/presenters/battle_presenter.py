class BattlePresenter:
    def __init__(self):
        pass

    def attack_result(self, result, enemy_name):    
        message = ""
        if result.crit:
            message += f"\nYou attack with an excellent attack!!\n"
        else:
            message += f"\nYou attack!\n"

        if result.dodge and not result.crit:
            message += f"But the {enemy_name} dodged your attack!\n"
        else:
            message += f"You hit {enemy_name} for {result.damage} points of damage!\n"

        return message