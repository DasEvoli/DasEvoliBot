# This collection of functions are special functions that can happen during the fight
# Lambda functions will call them most of them
# It gives us the freedom to make every kind of event happen

import asyncio
import random
import utils
import games.fight.attack_strings

    # Changes the hp value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_hp(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** ist immun 🛡.")
        return
    player.hp += value
    await ctx.send("**"+player.name+"**"+" hat jetzt ***"+str(player.hp)+" HP***")

    # Changes the hp value of players if they don't have an exception
    # Count means how many players are affected. -1 changes the hp value for every player
    # Does not work if the player is immune
async def change_players_hp(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** ist immun 🛡.")
                continue
            player.hp += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** ist immun 🛡.")
                continue
            player.hp += value
            await ctx.send("**"+player.name+"**"+" hat jetzt ***"+str(player.hp)+" HP***")

    # Changes the dodge value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_dodge(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** ist immun 🛡.")
        return
    player.dodge += value
    await ctx.send("**"+player.name+"**"+" hat jetzt einen Dodgewert von ***"+str(player.dodge)+"***")

    # Changes the attack value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_attack(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** ist immun 🛡.")
        return
    player.attack += value
    await ctx.send("**"+player.name+"**"+" hat jetzt einen Angriffswert von ***"+str(player.attack)+"***")

    # Changes the immune value of a player
    # This function is only if it happens for one player (special)
    # Can't be immune to that. Immune value gets increased instead
async def change_player_immune(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** ist immun 🛡.")
        return
    player.immune += value
    await ctx.send("**" + player.name + "** ist für " + "***"+str(value)+" Runden immun*** 🛡.")

    # Changes the immune value of a player
    # This function is only if it happens for one player (special)
    # Does not work if the player is immune
async def change_player_stun(ctx, player, value):
    if player.immune > 0:
        await ctx.send("**"+player.name+"** ist immun 🛡.")
        return
    player.stun += value
    await ctx.send("**" + player.name + "** ist für " + "***"+str(value)+" Runden gestunnt*** 😴.")


    # Changes the stun value of players if they don't have an exception
    # Count means how many players are affected. -1 changes the stun value for every player
    # Does not work if the player is immune
async def change_players_stun(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** ist immun 🛡.")
                continue
            player.stun += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** ist immun 🛡.")
                continue
            player.stun += value
            await ctx.send("**"+player.name+"**"+" ist jetzt ***"+str(value)+" Runden gestunnt*** 😴")

    # Changes the dodge value of players if they don't have an exception
    # Count means how many players are affected. -1 changes the dodge value for every player
    # Does not work if the player is immune
async def change_players_dodge(ctx, alive_players, value, count, attacker_player=None, exception=None):
    if count == -1:
        for player in alive_players:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** ist immun 🛡.")
                continue
            player.dodge += value
    else:
        for player in alive_players[:count]:
            if player == exception:
                continue
            if player.immune > 0:
                await ctx.send("**"+player.name+"** ist immun 🛡.")
                continue
            player.dodge += value
            await ctx.send("**"+player.name+"**"+" hat jetzt einen Dodgewert von ***"+str(player.dodge)+"***")


    # Revives dead players
    # -1 means all players get revived
async def revive_players(ctx, alive_players, all_players, value, count):
    if count == -1:
        for player in all_players:
            if player not in alive_players:
                player.hp = value
                player.stun = 0
                player.immun = 0
                alive_players.append(player)
                await ctx.send("**" + player.name + "**" + " wurde ***wiederbelebt*** mit*** "+str(value)+" HP***")
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

    await ctx.send("**" + player.name + "** was ist das Ergebnis von " + str(summand_one) + " * " + str(factor_one) + " - " + str(subtrahend_one))
    try:
        answer = await utils.bot.wait_for('message', timeout=10, check=lambda answer: answer.author.name == player.name)
    except asyncio.TimeoutError:
        await ctx.send("Zeit abgelaufen! Nächstes mal etwas mehr üben!")
        return
    if result == int(answer.content):
        await ctx.send("Wow, wir haben ein Mathegenie! Du wirst geheilt für ***" + str(value) + "***")
        if player.immune > 0:
            await ctx.send("**" + player.name + "** ist immun.")
            return
        player.hp += value
    else:
        await ctx.send("Das Ergebnis ist falsch :( Es wäre: **" + str(result) + "** gewesen")


# That is the standard when no special/event/shop etc. happens
# Important note: Also the bonus attack values are slighty random (by 1 - 5). This made it more unpredictable and fun
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
        await ctx.send("🛡**" + defender.name + "** ist Immun 🛡")
        return
    
    # The defender also has the chance to dodge the attack to add more randomness
    if random.randint(1, 100) <= defender.dodge:
        await ctx.send("**" + defender.name + "**" + " 🤸  weicht der Attacke aus!")
        return
    # Defender loses HP if he isn't immune or didn't dodge the attack
    defender.hp -= int(damage)
