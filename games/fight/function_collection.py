# This collection of functions that can happen during the fight
# Lambda functions will call most of them
# It gives us the freedom to make every kind of event happen

import asyncio
import random
import settings
import games.fight.attack_strings

# Changes the hp value of a player
# Does not work if the player is immune
async def change_player_hp(ctx, player, value):
    if player.immune_rounds > 0:
        await ctx.send("**"+ player.name +"** is immune 🛡")
        return
    player.hp += value
    await ctx.send("**"+ player.name +"**"+" has now ***"+str(player.hp)+" HP***")

# Changes the hp value of players if they don't have an exception
# Does not work if the player is immune
async def change_players_hp(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune_rounds > 0:
                await ctx.send("**"+player.name +"** is immune 🛡")
                continue
            player.hp += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune_rounds > 0:
                await ctx.send("**"+player.name +"** is immune 🛡")
                continue
            player.hp += value

# Changes the dodge value of a player
async def change_player_dodge(ctx, player, value):
    player.dodge += value
    await ctx.send("**"+ player.name +"**"+" has now a dodge value of ***"+str(player.dodge)+"***")

# Changes the attack value of a player
async def change_player_attack(ctx, player, value):
    player.attack += value
    await ctx.send("**"+ player.name +"**"+" has now an attack value of ***"+str(player.attack)+"***")

# Changes the immune value of a player
async def change_player_immune(ctx, player, value):
    player.immune_rounds += value
    await ctx.send("**" + player.name + "** is now " + "***"+str(value)+" rounds immune*** 🛡")

# Changes the stun value of a player
async def change_player_stun(ctx, player, value):
    player.stun_rounds += value
    await ctx.send("**" + player.name + "** is for " + "***"+str(value)+" rounds stunned*** 😴")


# Changes the stun value of players if they don't have an exception
async def change_players_stun(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            player.stun_rounds += value
            await ctx.send("**"+ player.name +"**"+" is now ***"+str(value)+" rounds stunned*** 😴")
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            player.stun_rounds += value
            await ctx.send("**"+ player.name +"**"+" is now ***"+str(value)+" rounds stunned*** 😴")

# Changes the dodge value of players.
#TODO: Add that a certain amount of players instead of just -1 for all.
async def change_players_dodge(ctx, alive_players, value, count, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            player.dodge += value
            await ctx.send("**" + player.name + "**" + " has now a dodge value of ***"+str(player.dodge) + "***")
            
# Revives dead players.
#TODO: Add that a certain amount of players get revived. Needs a death list.
async def revive_players(ctx, alive_players, all_players, value, count):
    if count == -1:
        for player in all_players:
            if player not in alive_players:
                player.hp = value
                player.stun_rounds = 0
                player.immune_rounds = 0
                alive_players.append(player)
                await ctx.send("**" + player.name + "**" + " was ***revived*** with*** "+str(value)+" HP***")

# Item
# If the player chooses this item he has to solve a small equation in a limited time
# If the solution is right the player gets healed
async def math_book(ctx, player, value):
    summand = random.randint(0, 99)
    factor = random.randint(1, 9)
    subtrahend = random.randint(0, 50)
    result = summand * factor - subtrahend
    await ctx.send("**" + player.name + "** what's the result of " + str(summand) + " * " + str(factor) + " - " + str(subtrahend))
    try:
        answer = await settings.bot.wait_for('message', timeout=settings.math_wait_timer, check=lambda answer: answer.author.name == player.name)
    except asyncio.TimeoutError:
        await ctx.send("Time is over.")
        return
    if result == int(answer.content):
        await ctx.send("Wow, insane math skills! You are getting healed for ***" + str(value) + "***")
        player.hp += value
    else:
        await ctx.send("The solution was wrong. It was: **" + str(result) + "**")

# This is the standard when no special/event happens
async def normal_attack(ctx, attacker, defender):
    attack_value = attacker.attack
    if random.randint(1, 100) <= attacker.crit_chance:
        damage = (attack_value - random.randint(1, 5)) * attacker.crit_multiplier
        await ctx.send(random.choice(games.fight.attack_strings.listAttackCrit).format(attacker=attacker.name, defender=defender.name, value=str(int(damage))))
    else:
        damage = attack_value - random.randint(1, 5)
        await ctx.send(random.choice(games.fight.attack_strings.listAttackNoCrit).format(attacker=attacker.name, defender=defender.name, value=str(damage)))
    if defender.immune_rounds > 0:
        await ctx.send("**" + defender.name + "** is immune 🛡")
        return
    if random.randint(1, 100) <= defender.dodge:
        await ctx.send("**" + defender.name + "**" + " 🤸 dodges the attack!")
        return
    defender.hp -= int(damage)
