from games.fight import settings

# Player object so every player has its own instance for attack damage and other stats
# *_rounds attributes get changed per round
# TODO: We save the username. Might be better to save the id instead
class Player:
    def __init__(self, name, userid, user):
        self.name = name
        self.hp = settings.basis_hp
        self.user = user
        self.stun_rounds = 0
        self.immune_rounds = 0
        self.dodge = settings.dodge
        self.attack = settings.attack
        self.crit_chance = settings.crit_chance
        self.crit_multiplier = settings.crit_multiplier