import random
import asyncio
from games.fight import jsoncontroller, function_collection, shop, event, special, settings, player

class Fight:

    def __init__(self, ctx, fighter_list, all_online):
        self.ctx = ctx
        self.tmp_fighter_list = fighter_list
        self.all_online = all_online
        self.current_round = 1
        self.all_players = []
        self.alive_players = []
        # We choose the next attacker randomly but he can never attack twice. We found it more fun to prevent that
        self.last_attacker = None

    def init_players(self):
        return_player_list = []
        for fighter in self.tmp_fighter_list:
            fighter_obj = player.Player(fighter.name, fighter.id, fighter)
            return_player_list.append(fighter_obj)
        self.tmp_fighter_list.clear()
        return return_player_list

    async def start(self):
        await self.ctx.send("Fight starts...")
        self.all_players = self.init_players()
        self.alive_players = self.all_players
        await self.setup_json()
        await self.fight_looper()

    # We save statistics of games in a json file that gets saved on the server.
    async def setup_json(self):
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

    # Every new round this looper gets called until all players are dead or only one is still alive
    async def fight_looper(self):
        while len(self.alive_players) > 1:
            string = "-----------------------------\n"
            for player in self.alive_players:
                string += "**" + player.name + ":**" + " ***{hp}hp  😴{stun_rounds}  🛡{immune_rounds}*** \n".format(hp=player.hp, stun_rounds=player.stun_rounds, immune_rounds=player.immune_rounds)
            await self.ctx.send(string)
            await asyncio.sleep(settings.default_delay)

            # Event
            if random.randint(1, 100) <= settings.event_chance:
                await event.start_event(self.ctx, self.all_players, self.alive_players)
                await self.update_deaths()
                await self.end_round()
                continue

            # Attacker
            attacker = random.choice(self.alive_players)
            while attacker == self.last_attacker:
                attacker = random.choice(self.alive_players)
            self.last_attacker = attacker
            await self.ctx.send("It's **" + attacker.name + "'s**" + " turn")

            await asyncio.sleep(settings.default_delay)

            # Check if attacker is stunned
            if attacker.stun_rounds > 0:
                await self.ctx.send("**" + attacker.name + "**" + " is still stunned 😴")
                await self.end_round()
                continue

            await asyncio.sleep(settings.default_delay)

            # Shop
            if self.all_online:
                if random.randint(1, 100) <= settings.shop_chance:
                    await shop.enter(self.ctx, attacker)
                    await self.update_deaths()
                    if len(self.alive_players) < 2:
                        await self.end_round()
                    if attacker.hp < 1:
                        await self.end_round()

            # Defender
            defender = random.choice(self.alive_players)
            while defender == attacker:
                defender = random.choice(self.alive_players)

            # Attacker and Defender are getting announced in chat
            await self.ctx.send("**" + attacker.name + "**" + " attacks " + "**" + defender.name + "**")
            await asyncio.sleep(settings.default_delay)

            # Special
            # It chooses a random Special from special.py
            # Attacker can't attack himself with a special
            if random.randint(1, 100) <= settings.special_chance:
                await special.start_special(self.ctx, attacker, defender, self.alive_players, self.all_players)
                await self.update_deaths(attacker)
                await self.end_round()
                continue

            # Normal Attack
            await function_collection.normal_attack(self.ctx, attacker, defender)
            await self.update_deaths(attacker)
            await self.end_round()
            continue
        await self.end_game()

    async def end_game(self):
        if len(self.alive_players) <= 0:
            await self.ctx.send("😖**ALL PLAYERS ARE DEAD**😖")
            for player in self.all_players:
                jsoncontroller.add_lose(self.ctx.guild.name, player)

        else:
            winner = self.alive_players[0]
            await self.ctx.send("🏆 Congratulation Winner is **" + winner.name + "** 🏆")
            for player in self.all_players:
                if player != winner:
                    jsoncontroller.add_lose(self.ctx.guild.name, player)
            jsoncontroller.add_win(self.ctx.guild.name, winner)
  
    async def update_deaths(self, attacker=None):
        tmp_list = []
        for player in self.alive_players:
            if player.hp < 1:
                await self.ctx.send("💔**" + player.name + "** was destroyed💔")
                if attacker is None:
                    continue
                else:
                    await self.ctx.send("**" + attacker.name + "** has a new kill")
                    jsoncontroller.add_kill(self.ctx.guild.name, attacker)
                    continue
            else:
                tmp_list.append(player)
        self.alive_players = tmp_list

    async def end_round(self):
        await self.ctx.send("Round " + str(self.current_round) + " ended...")
        self.current_round += 1
        for player in self.alive_players:
            if player.immune_rounds > 0: player.immune_rounds -= 1
            if player.stun_rounds > 0: player.stun_rounds -= 1
        await asyncio.sleep(settings.default_delay)

