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

    def fleeing(self, succeed, enemy_name):
        self.view.update_output(None, f"You attempt to run away...\n")
        if succeed:
            self.view.update_output(None, f"You successfully flee!\n")
        else:
            self.view.update_output(None, f"""...but the {enemy_name} blocks you from running away!\n""")

    def no_spell_selected(self, spell):
        if spell == "Select Spell":
            self.view.update_output(None, "You must select a valid spell first.\n")
        else:
            self.view.update_output(None, "Your level is too low to cast magic.\n")

    def not_enough_mp(self, spell):
        self.view.update_output(None, f"Player tries to cast {spell}, but doesn't have enough MP!\n")

    def player_spellstopped(self, spell):
        self.view.update_output(None, f"""Player casts {spell}, but their magic has been sealed!\n""")

    def player_casts_heal_when_full(self, spell):
        self.view.update_output(None, f"""Player casts {spell}, but their hit points were already at maximum!\n""")

    def player_casts_heal(self, spell, amount):
        self.view.update_output(None, f"""Player casts {spell}! Player is healed {str(amount)} hit points!\n""")

    def enemy_resists_hurt(self, spell):
        self.view.update_output(None, f"""Player casts {spell}, but the enemy resisted!\n""")

    def player_casts_hurt(self, spell, enemy_name, amount):
        self.view.update_output(None, f"""Player casts {spell}! {enemy_name} is hurt by {str(amount)} hit points!\n""")

    def enemy_already_asleep(self, enemy_name):
        self.view.update_output(None, f"""Player casts Sleep! But the {enemy_name} is already asleep!\n""")

    def enemy_resists_sleep(self, enemy_name):
        self.view.update_output(None, f"""Player casts Sleep! But the {enemy_name} resisted!\n""")

    def enemy_now_asleep(self, enemy_name):
        self.view.update_output(None, f"""Player casts Sleep! The {enemy_name} is now asleep!\n""")
    
    def enemy_already_stopped(self, enemy_name):
        self.view.update_output(None, f"""Player casts Stopspell! But the {enemy_name}'s magic was already blocked!\n""")

    def enemy_resists_stopped(self, enemy_name):
        self.view.update_output(None, f"""Player casts Stopspell! But the {enemy_name} resisted!\n""")

    def enemy_now_spell_stopped(self, enemy_name):
        self.view.update_output(None, f"""Player casts Stopspell! The {enemy_name}'s magic is now blocked!!\n""")
