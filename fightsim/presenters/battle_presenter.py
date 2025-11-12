from ..common.messages import EnemyActions, SpellFailureReason

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

    def player_spell_failed(self, result, enemy_name):
        if result.reason == SpellFailureReason.NOT_ENOUGH_MP:
            self.view.update_output(None, f"Player tries to cast {result.spell_name}, but doesn't have enough MP!\n")
        elif result.reason == SpellFailureReason.PLAYER_SPELLSTOPPED:
            self.view.update_output(None, f"""Player casts {result.spell_name}, but their magic has been sealed!\n""")
        elif result.reason == SpellFailureReason.HEALED_AT_MAX_HP:
            self.view.update_output(None, f"""Player casts {result.spell_name}, but their hit points were already at maximum!\n""")
        elif result.reason == SpellFailureReason.ENEMY_RESISTED_HURT:
            self.view.update_output(None, f"""Player casts {result.spell_name}, but the enemy resisted!\n""")
        elif result.reason == SpellFailureReason.ENEMY_ALREADY_ASLEEP:
            self.view.update_output(None, f"""Player casts Sleep! But the {enemy_name} is already asleep!\n""")
        elif result.reason == SpellFailureReason.ENEMY_RESISTED_SLEEP:
            self.view.update_output(None, f"""Player casts Sleep! But the {enemy_name} resisted!\n""")
        elif result.reason == SpellFailureReason.ENEMY_ALREADY_SPELLSTOPPED:
            self.view.update_output(None, f"""Player casts Stopspell! But the {enemy_name}'s magic was already blocked!\n""")
        elif result.reason == SpellFailureReason.ENEMY_RESISTED_SPELLSTOP:
            self.view.update_output(None, f"""Player casts Stopspell! But the {enemy_name} resisted!\n""")


    def player_casts_heal(self, spell, amount):
        self.view.update_output(None, f"""Player casts {spell.name}! Player is healed {str(amount)} hit points!\n""")

    def player_casts_hurt(self, spell, enemy_name, amount):
        self.view.update_output(None, f"""Player casts {spell.name}! {enemy_name} is hurt by {str(amount)} hit points!\n""")

    def enemy_now_asleep(self, enemy_name):
        self.view.update_output(None, f"""Player casts Sleep! The {enemy_name} is now asleep!\n""")

    def enemy_now_spell_stopped(self, enemy_name):
        self.view.update_output(None, f"""Player casts Stopspell! The {enemy_name}'s magic is now blocked!!\n""")
    
    def player_is_sleeping(self):
        self.view.update_output(None, "You're still asleep...'\n")

    def player_woke_up(self):
        self.view.update_output(None, "You wake up!\n")

    def enemy_is_sleeping(self, enemy_name):
        self.view.update_output(None, f"The {enemy_name} is asleep...")
    
    def enemy_is_still_sleeping(self, enemy_name):
        self.view.update_output(None, f"The {enemy_name} is still asleep...")
    
    def enemy_woke_up(self, enemy_name):
        self.view.update_output(None, f"The {enemy_name} woke up!")

    def enemy_flees(self, enemy_name):
        self.view.update_output(None, f"The {enemy_name} flees the battlefield!")
    
    def enemy_attacks(self, enemy_name, amount):
        self.view.update_output(None, f"{enemy_name} attacks! {enemy_name} hits you for {amount} damage.\n")

    def enemy_wins(self, enemy_name):
        self.view.update_output(None, f"You have been defeated by the {enemy_name}!\n")

    def enemy_casts_while_spellstopped(self, enemy_name, spell):
        spell_name = ""
        if spell == EnemyActions.HURT:
            spell_name = "Hurt"
        if spell == EnemyActions.HURTMORE:
            spell_name = "Hurtmore"
        if spell == EnemyActions.HEAL:
            spell_name = "Heal"
        if spell == EnemyActions.HEALMORE:
            spell_name = "Healmore"
        if spell == EnemyActions.SLEEP:
            spell_name = "Sleep"
        if spell == EnemyActions.STOPSPELL:
            spell_name = "Stopspell"
        self.view.update_output(f"""The {enemy_name} casts {spell_name}, but their spell has been blocked!""")

    def enemy_casts_hurt(self, enemy_name, result, player_name):
        spell_name = ""
        damage = result[1]
        if result[0] == EnemyActions.HURT:
            spell_name = "Hurt"
        if result[0] == EnemyActions.HURTMORE:
            spell_name = "Hurtmore"
        self.view.update_output(f"""The {enemy_name} casts {spell_name}! {player_name} is hurt for {damage} damage!""")

    def enemy_breathes_fire(self, enemy_name, result, player_name):
        spell_name = ""
        damage = result[1]
        if result[0] == EnemyActions.FIRE:
            spell_name = "fire"
        if result[0] == EnemyActions.STRONGFIRE:
            spell_name = "strong flames at you!"
        self.view.update_output(f"""The {enemy_name} breathes {spell_name}! {player_name} is hurt for {damage} damage!""")

    def enemy_casts_heal(self, enemy_name, result):
        spell_name = ""
        heal_amt = result[1]
        if result[0] == EnemyActions.HEAL:
            spell_name = "Heal"
        if result[0] == EnemyActions.HEALMORE:
            spell_name = "Healmore"
        self.view.update_output(f"""The {enemy_name} casts {spell_name}! {enemy_name} is healed {heal_amt} hit points!""")

    def enemy_casts_sleep(self, enemy_name):
        self.view.update_output(f"""The {enemy_name} casts Sleep. You fall asleep!!""")

    def enemy_casts_stopspell(self, enemy_name, result):
        if result is False:
            self.view.update_output(f"""The {enemy_name} casts Spellstop, but the spell fails!""")
        else:
            self.view.update_output(f"""The {enemy_name} casts Spellstop. Your magic has been blocked!""")