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

        return message
    
    def start_fight_msg(self, _, enemy_name):
        self.view.main_frame.txt["state"] = 'normal'
        message = f"""You are fighting the {enemy_name}!\n"""
        self.view.update_output(None, message)
        

