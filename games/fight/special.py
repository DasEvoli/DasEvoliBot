# Attacker can roll a special while he attacks
# Specials can happen during a fight and is initiated by the attacker with a certain chance

import asyncio
import random
import discord
import os
from games.fight import function_collection, settings


async def start_special(ctx, attacker, defender, alive_players, all_players):
    # [0] = String that gets sent when this special is happening
    # [1] = Lambda Function that will happen if that event gets chosen
    # [2] = Value of that special
    # [3] = Kind of attack. -1 = affects all players, 0 = affects himself, 1 = affects the defender. This value gets never used. It's only for yourself as documentation
    # [4] = Image of that event
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    listSpecials = [
        [
            "**{attacker}** uses cuddling and squeezes **{defender}** all her/his air out ***{value} damage*** to **{defender}**",
            lambda: function_collection.change_player_hp(ctx, defender, -30),
            30,
            1,
            curr_dir + settings.dir_special + "fluffy.gif"
        ],
        [
            "**{attacker}** has to rest and places something on the ground. A big dome surrounds him/her. ***{attacker}*** is "
            "***immune*** for ***{value} rounds***",
            lambda: function_collection.change_player_immune(ctx, attacker, 4),
            4,
            0,
            curr_dir + settings.dir_special + "gibraltar.jpg"
        ],
        [
            "**{attacker}** sees, that all players stand together. An artillery attack ***{value} damage***"
            " to **EVERYONE except {attacker}**",
            lambda: function_collection.change_players_hp(ctx, alive_players, -15, -1, exception=attacker),
            15,
            -1,
            curr_dir + settings.dir_special + "artillerie.jpg"
        ],
        [
            "**{attacker}** punshes a tunnel. Hiding in the void no one can hit him/her. ***immune for {value} rounds***",
            lambda: function_collection.change_player_immune(ctx, attacker, 3),
            3,
            0,
            curr_dir + settings.dir_special + "void.jpg"
        ],
        [
            "**{attacker}**: Bambazoo...Bamba... Bambamala.. fool em **{attacker}** sends a clone and fools his/her enemies. "
            "Immune for ***{value}*** rounds",
            lambda: function_collection.change_player_immune(ctx, attacker, 3),
            3,
            0,
            curr_dir + settings.dir_special + "bamboozled.jpg"
        ],
        [
            "**{attacker}** hides in a corner and waits for **{defender}**. Years passed. "
            "***{value} damage*** to **{attacker}**",
            lambda: function_collection.change_player_hp(ctx, attacker, -20),
            20,
            0,
            curr_dir + settings.dir_special + "camper.jpg"
        ],
        [
            "**{attacker}** feels like an adult, but is only 17 years old. Stun for ***{value} rounds***",
            lambda: function_collection.change_player_stun(ctx, attacker, 4),
            4,
            0,
            curr_dir + settings.dir_special + "teen.jpg"
        ],
        [
            "**{attacker}** walks slowly. IT'S HIGH NOON...DRAW ***{value} damage*** to **EVERYONE except {attacker}**",
            lambda: function_collection.change_players_hp(ctx, alive_players, -15, -1, exception=attacker),
            15,
            -1,
            curr_dir + settings.dir_special + "highnoon.gif"
        ],
        [
            "**{attacker}** has enough and takes out a letter. AN ACCUSATION FOR COPYRIGHT **{defender}** "
            "never heard about article 13 and gets {value} years into prison ***stun*** "
            "for ***{value} rounds***",
            lambda: function_collection.change_player_stun(ctx, defender, 4),
            4,
            1,
            curr_dir + settings.dir_special + "article13.jpg"
        ]
    ]
    # We announce the event with a string that gets attacker and defender as input
    special = random.choice(listSpecials)
    await ctx.send(str(special[0]).format(value=special[2], attacker=attacker.name, defender=defender.name))
    await ctx.send(file=discord.File(special[4]))
    await asyncio.sleep(settings.default_delay)
    await special[1]()
