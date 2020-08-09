# This collection of functions are special functions that can happen during the fight
# Lambda functions will call them most of them
# It gives us the freedom to make every kind of event happen

import asyncio
import random
import settings
import games.fight.attack_strings

    # Changes the hp value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_hp(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** is immune 🛡.")
        return
    player.hp += value
    await ctx.send("**"+player.name+"**"+" has now ***"+str(player.hp)+" HP***")

    # Changes the hp value of players if they don't have an exception
    # Count means how many players are affected. -1 changes the hp value for every player
    # Does not work if the player is immune
async def change_players_hp(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** is immune 🛡.")
                continue
            player.hp += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** is immune 🛡.")
                continue
            player.hp += value
            await ctx.send("**"+player.name+"**"+" has now ***"+str(player.hp)+" HP***")

    # Changes the dodge value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_dodge(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** is immune 🛡.")
        return
    player.dodge += value
    await ctx.send("**"+player.name+"**"+" has now a dodge value of ***"+str(player.dodge)+"***")

    # Changes the attack value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_attack(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** is immune 🛡.")
        return
    player.attack += value
    await ctx.send("**"+player.name+"**"+" has now an attack value of ***"+str(player.attack)+"***")

    # Changes the immune value of a player
    # This function is only if it happens for one player (special)
    # Can't be immune to that. Immune value gets increased instead
async def change_player_immune(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** is immune 🛡.")
        return
    player.immune += value
    await ctx.send("**" + player.name + "** is now " + "***"+str(value)+" rounds immune*** 🛡.")

    # Changes the immune value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_stun(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** is immune 🛡.")
        return
    player.stun += value
    await ctx.send("**" + player.name + "** is for " + "***"+str(value)+" rounds stunned*** 😴.")


    # Changes the stun value of players if they don't have an exception
    # Count means how many players are affected. -1 changes the stun value for every player
    # Does not work if the player is immune
async def change_players_stun(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** is immune 🛡.")
                continue
            player.stun += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** is immune 🛡.")
                continue
            player.stun += value
            await ctx.send("**"+player.name+"**"+" is now ***"+str(value)+" rounds stunned*** 😴")

    # Changes the dodge value of players if they don't have an exception
    # Count means how many players are affected. -1 changes the dodge value for every player
    # Does not work if the player is immune
async def change_players_dodge(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** is immune 🛡.")
                continue
            player.dodge += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** is immune 🛡.")
                continue
            player.dodge += value
            await ctx.send("**"+player.name+"**"+" has now a dodge value of ***"+str(player.dodge)+"***")


    # Revives dead players
    # -1 means all players get revived
async def revive_players(ctx, alive_players, all_players, value, count):
    if count == -1:
        for player in all_players:
            if player not in alive_players:
                player.hp = value
                player.stun = 0
                player.immune = 0
                alive_players.append(player)
                await ctx.send("**" + player.name + "**" + " was ***revived*** with*** "+str(value)+" HP***")
    else:
        pass # TODO: add feature that 3 random players get revived. Maybe create a death list

    # Item
    # If the player chooses this item he has to solve a small equation in a limited time
    # If the solution is right the player gets healed

async def math_book(ctx, player, value):

    summand_one = random.randint(0, 99)
    factor_one = random.randint(1, 9)
    subtrahend_one = random.randint(0, 50)

    result = summand_one * factor_one - subtrahend_one

    await ctx.send("**" + player.name + "** what's the result of " + str(summand_one) + " * " + str(factor_one) + " - " + str(subtrahend_one))
    try:
        answer = await settings.bot.wait_for('message', timeout=10, check=lambda answer: answer.author.name == player.name)
    except asyncio.TimeoutError:
        await ctx.send("Time is over! Next time practice more!")
        return
    if result == int(answer.content):
        await ctx.send("Wow, insane math skills! You are getting healed for ***" + str(value) + "***")
        if player.immune > 0:
            await ctx.send("**" + player.name + "** is immune")
            return
        player.hp += value
    else:
        await ctx.send("The solution was wrong :( It was: **" + str(result) + "**")


# That is the standard when no special/event/shop etc. happens
# Important note: Also the bonus attack values are slightly random (by 1 - 5). This made it more unpredictable and fun
async def normal_attack(ctx, attacker, defender):

    attack_value = attacker.attack
    # Attacker is able to crit by his critchance
    if random.randint(1, 100) <= attacker.critchance:
        damage = (attack_value - random.randint(1, 5)) * attacker.critmultiplier
        # Random String gets sent in chat
        await ctx.send(
            random.choice(games.fight.attack_strings.listAttackCrit).format(attacker=attacker.name,
                                                     defender=defender.name,
                                                     value=str(int(damage))))
        await asyncio.sleep(1)
    # Attacker didn't crit
    else:
        damage = attack_value - random.randint(1, 5)
        await ctx.send(
            random.choice(games.fight.attack_strings.listAttackNoCrit).format(attacker=attacker.name,
                                                       defender=defender.name,
                                                       value=str(damage)))
        await asyncio.sleep(1)

    # Now it checks if the defender is immune. If so the attack has no effect
    if defender.immune > 0:
        await ctx.send("🛡**" + defender.name + "** is immune 🛡")
        return
    
    # The defender also has the chance to dodge the attack to add more randomness
    if random.randint(1, 100) <= defender.dodge:
        await ctx.send("**" + defender.name + "**" + " 🤸  dodges the attack!")
        return
    # Defender loses HP if he isn't immune or didn't dodge the attack
    defender.hp -= int(damage)
