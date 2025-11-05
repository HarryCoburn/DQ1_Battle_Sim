class BattlePresenter:
    def __init__(self, view):
        self.view = view

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
        self.view.update_output(None, message)
    
    def start_fight_msg(self, _, enemy_name):
        self.view.main_frame.txt["state"] = 'normal'
        message = f"""You are fighting the {enemy_name}!\n"""
        self.view.update_output(None, message)
        

    def player_surprised(self, _, enemy_name):
        message = f"""The {enemy_name} surprises you! They attack first!\n"""
        self.view.update_output(None, message)

    def player_wins(self, _, enemy_name):
        message = f"""You have defeated the {enemy_name}!\n"""
        self.view.update_output(None, message)

    def no_herbs(self):
        message = "You have no herbs!\n"
        self.view.update_output(None, message)

    def eat_herb_at_full_hp(self):
        message = "You eat a herb, but your hit points are already at maximum!\n"
        self.view.update_output(None, message)

    def eat_herb(self, _, heal_amt):
        message = f"""You eat a herb and regain {heal_amt} hit points!\n"""
        self.view.update_output(None, message)