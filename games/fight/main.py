# Main function for the fight module

import random
import asyncio
import games.fight.jsoncontroller
import games.fight.shop
import games.fight.event
import games.fight.special
import games.fight.function_collection

# Easy to adjust values
# Chances are always in %
basis_hp = 100
eventchance = 5 
specialchance = 15
shopchance = 10


class Fight:
    # Round starts by one
    current_round = 1
    # List to store all players
    all_players = []  
    # List to store only players for are still alive
    alivePlayers = []
    # Not a must-have. We choose the next attacker randomly but it is never the last attacker. We found it more fun to prevent that
    last_attacker = None

    def __init__(self, ctx, fighterlist, all_online):
        self.fighterlist = fighterlist
        self.ctx = ctx
        self.all_online = all_online

    # We create an object for every player and store them in a list. fighterlist will not be used from now on.
    def init_players(self):
        return_player_list = []
        for player in self.fighterlist:
            player_obj = Player(player.name, basis_hp, player.id, player)
            return_player_list.append(player_obj)
        self.fighterlist.clear()
        return return_player_list


    # This function gets called in dasevolibot.py by using the command "$fight"
    async def start(self):
        await self.ctx.send("Fight gets started...")
        self.all_players = self.init_players()
        self.alivePlayers = self.all_players

        # We save statistics in json
        # Json data is seperated per server. That means a user can have different statistics per server
        if not games.fight.jsoncontroller.check_file_exists():
            games.fight.jsoncontroller.create_file()
        if not games.fight.jsoncontroller.check_server_exists(self.ctx.guild.name):
            games.fight.jsoncontroller.add_server(self.ctx.guild.name)
        for player in self.all_players:
            if games.fight.jsoncontroller.check_player_exists(self.ctx.guild.name, player):
                games.fight.jsoncontroller.add_game(self.ctx.guild.name, player)
            else:
                games.fight.jsoncontroller.add_new_player(self.ctx.guild.name, player)
                games.fight.jsoncontroller.add_game(self.ctx.guild.name, player)
        # Preperation is now over. Game starts finally
        await self.fight_looper()

    # In that loop the fight is happening. Every new round this looper gets called until all players are dead or only one is still alive
    async def fight_looper(self):
        # While at least 2 players are alive the next round starts
        while len(self.alivePlayers) > 1:
            # Overview in chat about all players, their life and other stats
            string = ""
            string += "-----------------------------\n"
            for player in self.alivePlayers:
                string += "**" + player.name + ":**" + " ***{hp}hp  😴{stun}  🛡{immune}*** \n".format(hp=player.hp, stun=player.stun, immune=player.immune)
            await self.ctx.send(string)
            await asyncio.sleep(2)

            # event
            # Depending on the chances we check if an event should happen
            if random.randint(1, 100) <= eventchance:
                await games.fight.event.start_event(self.ctx, self.all_players, self.alivePlayers)
                # We need to check deaths because it's possible that an event kills a player or even all. No Argument because an event means no player attacked
                await self.check_deaths()
                # An event means that the round ends. Continue the loop
                await self.end_round()
                continue

            # Attacker
            # Gets chosen randomly and can't be the same two times in a row
            attacker = random.choice(self.alivePlayers)
            while attacker == self.last_attacker:
                attacker = random.choice(self.alivePlayers)
            self.last_attacker = attacker
            await self.ctx.send("It's **" + attacker.name + "'s**" + " turn!")
            await asyncio.sleep(2)

            # Check if attacker is stunned
            # If true nothing happens and the round ends
            if attacker.stun > 0:
                await self.ctx.send("**" + attacker.name + "**" + " is still in stun! 😴")
                await self.end_round()
                continue
            await asyncio.sleep(1)

            # Defender
            # Gets chosen randomly. Can be the same multiple times in a row!
            # Attacker can't be defender in the same time
            defender = random.choice(self.alivePlayers)
            while defender == attacker:
                defender = random.choice(self.alivePlayers)

            # Shop
            # Works only if all players are online
            # Can also happen randomly. Some items need interaction from the user (like mathbook)
            # Only the attacker can enter the shop
            if self.all_online:
                if random.randint(1, 100) <= shopchance:
                    await games.fight.shop.enter(self.ctx, attacker)
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
            if random.randint(1, 100) <= specialchance:
                await games.fight.special.start_special(self.ctx, attacker, defender, self.alivePlayers, self.all_players)
                await self.check_deaths(attacker)
                await self.end_round()
                continue

            # Attack
            # That is the standard when no special/event/shop etc. happens
            await games.fight.function_collection.normal_attack(self.ctx, attacker, defender)
            await self.check_deaths(attacker)
            await self.end_round()
        # Less than 2 players are alive. Game ends now
        await self.end_game()

    async def end_game(self):
        if len(self.alivePlayers) == 0:
            await self.ctx.send("😖**ALL PLAYERS ARE DEAD**😖")
            for player in self.all_players:
                games.fight.jsoncontroller.add_lose(self.ctx.guild.name, player)

        else:
            await self.ctx.send("🏆 Congratulation! Winner is **" + self.alivePlayers[0].name + "**! 🏆 ")

            for player in self.all_players:
                if player != self.alivePlayers[0]:
                    games.fight.jsoncontroller.add_lose(self.ctx.guild.name, player)

            games.fight.jsoncontroller.add_win(self.ctx.guild.name, self.alivePlayers[0])

    
    # Check for HP and remove the player from the game
    # Death gets added to json
    # If attacker is defined then the attacker gets a kill
    # TODO I'm not sure why I need this tmp_list. I can remember that I used it as a fix
    async def check_deaths(self, attacker=None):
        tmp_list = []
        for player in self.alivePlayers:
            if player.hp < 1:
                await self.ctx.send("💔**" + player.name + "** was destroyed!💔")
                if attacker is None:
                    continue
                else:
                    await self.ctx.send("**" + attacker.name + "** has a new kill!")
                    games.fight.jsoncontroller.add_kill(self.ctx.guild.name, attacker)
                    continue
            else:
                tmp_list.append(player)
        self.alivePlayers = tmp_list

    # New round gets started
    # Effects like immunity are getting decreased by 1
    async def end_round(self):
        await self.ctx.send("Round " + str(self.current_round) + " ended...")
        self.current_round += 1
        for player in self.alivePlayers:
            if player.immune > 0: player.immune -= 1
            if player.stun > 0: player.stun -= 1


    # Player object so every player has its own instance for attack damage and other stats
    # This object will also be stored in a list when the game starts
class Player:
    # these attributes get changed per round if they are > 0
    stun = 0
    immune = 0
    # basic stats
    dodge = 15
    attack = 15
    critchance = 20
    critmultiplier = 1.6


    def __init__(self, name, hp, userid, user):
        self.name = name
        self.hp = hp
        self.user = user
