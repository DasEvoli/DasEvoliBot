import random
import asyncio
from games.fight import jsoncontroller, function_collection, shop, event, special, settings

class Fight:

    def __init__(self, ctx, fighter_list, all_online):
        self.ctx = ctx
        self.tmp_fighter_list = fighter_list
        self.all_online = all_online
        self.current_round = 1
        self.all_players = []
        self.alive_players = []
        # Not a must-have. We choose the next attacker randomly but he can never attack twice. We found it more fun to prevent that
        self.last_attacker = None

    def init_players(self):
        return_player_list = []
        for player in self.tmp_fighter_list:
            player_obj = Player(player.name, player.id, player)
            return_player_list.append(player_obj)
        self.tmp_fighter_list.clear()
        return return_player_list

    async def start(self):
        await self.ctx.send("Fight starts...")
        self.all_players = self.init_players()
        #TODO is this correct? We reference the list. In the end all_players should not be different than alive_players
        self.alive_players = self.all_players

        # TODO Refactor. For example putting the fight setup in one seperate func
        # We save statistics of games in a json file that gets saved on the server
        if not jsoncontroller.statistic_file_exists():
            jsoncontroller.create_statistic_file()
        if not jsoncontroller.check_server_exists(self.ctx.guild.name):
            jsoncontroller.add_server(self.ctx.guild.name)
        for player in self.all_players:
            if jsoncontroller.check_player_exists(self.ctx.guild.name, player):
                jsoncontroller.add_game(self.ctx.guild.name, player)
            else:
                jsoncontroller.add_new_player(self.ctx.guild.name, player)
                jsoncontroller.add_game(self.ctx.guild.name, player)
        await self.fight_looper()

    # Every new round this looper gets called until all players are dead or only one is still alive
    async def fight_looper(self):
        while len(self.alive_players) > 1:
            string = "-----------------------------\n"
            for player in self.alive_players:
                string += "**" + player.name + ":**" + " ***{hp}hp  😴{stun_rounds}  🛡{immune_rounds}*** \n".format(hp=player.hp, stun_rounds=player.stun_rounds, immune_rounds=player.immune_rounds)
            await self.ctx.send(string)
            await asyncio.sleep(2) # TODO constant refactor to setting file

            # Event
            if random.randint(1, 100) <= settings.event_chance:
                await event.start_event(self.ctx, self.all_players, self.alive_players)
                await self.check_deaths()
                await self.end_round()
                continue

            # Attacker
            # Gets chosen randomly and can't be the same two times in a row
            attacker = random.choice(self.alive_players)
            while attacker == self.last_attacker: #TODO This is ugly
                attacker = random.choice(self.alive_players)
            self.last_attacker = attacker
            await self.ctx.send("It's **" + attacker.name + "'s**" + " turn!")
            await asyncio.sleep(2)

            # Check if attacker is stunned
            if attacker.stun_rounds > 0:
                await self.ctx.send("**" + attacker.name + "**" + " is still stunned! 😴")
                await self.end_round()
                continue
            await asyncio.sleep(1)

            # Defender
            # Gets chosen randomly. Can be the same multiple times in a row but can't be attacker at the same time
            defender = random.choice(self.alive_players)
            while defender == attacker: #TODO also must be fixed
                defender = random.choice(self.alive_players)

            # Shop
            # Only the attacker can enter the shop
            if self.all_online:
                if random.randint(1, 100) <= settings.shop_chance:
                    await shop.enter(self.ctx, attacker)
                    # LAST TIME HERE
                    # Need to check if attacker is dead because there are actually items that can hurt you
                    await self.check_deaths(attacker)
                    await self.end_round()
                    continue

            # Attacker and Defender are getting announced in chat
            await self.ctx.send("**" + attacker.name + "**" + " attacks " + "**" + defender.name + "**!")
            await asyncio.sleep(2)

            # Special
            # Can happen randomly
            # It chooses a random Special from special.py
            if random.randint(1, 100) <= settings.special_chance:
                await special.start_special(self.ctx, attacker, defender, self.alive_players, self.all_players)
                await self.check_deaths(attacker)
                await self.end_round()
                continue

            # Attack
            # That is the standard when no special/event/shop etc. happens
            await function_collection.normal_attack(self.ctx, attacker, defender)
            await self.check_deaths(attacker)
            await self.end_round()
        # Less than 2 players are alive. Game ends now
        await self.end_game()

    async def end_game(self):
        if len(self.alive_players) == 0:
            await self.ctx.send("😖**ALL PLAYERS ARE DEAD**😖")
            for player in self.all_players:
                jsoncontroller.add_lose(self.ctx.guild.name, player)

        else:
            await self.ctx.send("🏆 Congratulation! Winner is **" + self.alive_players[0].name + "**! 🏆 ")

            for player in self.all_players:
                if player != self.alive_players[0]:
                    jsoncontroller.add_lose(self.ctx.guild.name, player)

            jsoncontroller.add_win(self.ctx.guild.name, self.alive_players[0])

    
    # TODO I'm not sure why I need this tmp_list. I can remember that I used it as a fix
    async def check_deaths(self, attacker=None):
        tmp_list = []
        for player in self.alive_players:
            if player.hp < 1:
                await self.ctx.send("💔**" + player.name + "** was destroyed!💔")
                if attacker is None:
                    continue
                else:
                    await self.ctx.send("**" + attacker.name + "** has a new kill!")
                    jsoncontroller.add_kill(self.ctx.guild.name, attacker)
                    continue
            else:
                tmp_list.append(player)
        self.alive_players = tmp_list

    # New round gets started
    # Effects like immunity are getting decreased by 1
    async def end_round(self):
        await self.ctx.send("Round " + str(self.current_round) + " ended...")
        self.current_round += 1
        for player in self.alive_players:
            if player.immune_rounds > 0: player.immune_rounds -= 1
            if player.stun_rounds > 0: player.stun_rounds -= 1


    # Player object so every player has its own instance for attack damage and other stats
    # *_rounds attributes get changed per round
    # TODO We save the username. Might be better to save the id instead
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
