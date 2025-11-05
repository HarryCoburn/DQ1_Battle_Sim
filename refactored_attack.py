# A refactoring of player_attack and its chain

# First, the player click the attack button
# BattleFrame intercepts this event through Tkinter and now calls Controller.on_attack_button()

#In Controller controller
# a new function:

def on_attack_button(self):
    result = self.battle.player_attack() # Domain logic in battle called to get a hit and a result. We assume a normal hit for simplicity.

    if result.hit:
        self.model.enemy.take_damage(result.damage)
        message = self.format_attack_message(result, self.battle.enemy.name)
        self.view.update_output(message)
        self.view.update_enemy_info(self.battle.enemy) # We want the battle version here so that when the battle is done it can be discarded and the model enemy can come right back in for another battle.

def format_attack_result(result, enemy_name):    
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


# In Battle controller
def player_attack(self, *_):
    """ Refactored version of my player attack program. """
    crit = self.check_for_player_critical_hit() # We assume this is present
    dodge = self.check_For_enemy_dodge() # We assume this is present
    damage = self.calculate_player_attack_damage(crit) # We assume this is present

    return AttackResult(
        crit=crit,
        dodge=dodge,
        damage=damage,
        hit = not (dodge and not crit)
    )

# View functions remain the same

