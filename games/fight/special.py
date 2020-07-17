# Attacker can roll a special while he attacks
# Image will be posted
# It can also be a negative special

import asyncio
import random
import settings
import games.fight.function_collection as function_collection
import discord

# Important to make those variables global so we can use lambda functions in a list
alive_players_global = []
all_players_global = []
current_ctx_global = None
attacker_global = None
defender_global = None

async def start_special(ctx, attacker, defender, alive_players, all_players):
    global alive_players_global, all_players_global, current_ctx_global, attacker_global, defender_global
    all_players_global = all_players
    alive_players_global = alive_players
    current_ctx_global = ctx
    attacker_global = attacker
    defender_global = defender

    # Random special gets chosen
    special = random.choice(listSpecials)
    # Sends index 0, which is the special message, in chat
    await ctx.send(str(special[0]).format(value=special[2], attacker=attacker_global.name, defender=defender_global.name))
    # We always also send an image when a special happens. That's important
    await ctx.send(file=discord.File(special[4]))
    await asyncio.sleep(2)
    # With that we call the lambda function in a list
    # We use that so it's much easier and much more customable to make cool events. Literally everything possible
    await special[1]()


# [0] = Text of that special that gets posted in chat
# [1] = Lambda Function that will happen if that event gets chosen
# [2] = Value of that special
# [3] = Kind of attack. -1 = affects all players, 0 = affects himself, 1 = affects the defender. This value gets never used. It's only for yourself.
# [4] = Image of that event

listSpecials = [
    [
        "**{attacker}** uses cuddling and squeezes **{defender}** all her/his air out! ***{value} damage*** to **{defender}**!",
        lambda: function_collection.change_player_hp(current_ctx_global, defender_global, -30),
        30,
        1,
        settings.dict_special + "fluffy.gif"
    ],
    [
        "**{attacker}** has to rest and places something on the ground. A big dome surrounds him. ***{attacker}*** is "
        "***immune*** for ***{value} rounds!***",
        lambda: function_collection.change_player_immune(current_ctx_global, attacker_global, 4),
        4,
        0,
        settings.dict_special + "gibraltar.jpg"
    ],
    [
        "**{attacker}** sees, that all players stand together. An artillery attack! ***{value} damage***"
        " to **EVERYONE except {attacker}**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -15, -1, exception=attacker_global),
        15,
        -1,
        settings.dict_special + "artillerie.jpg"
    ],
    [
        "**{attacker}** punshes a tunnel. Hiding in the void no one can hit him. ***immune for {value} rounds!***",
        lambda: function_collection.change_player_immune(current_ctx_global, attacker_global, 3),
        3,
        0,
        settings.dict_special + "void.jpg"
    ],
    [
        "**{attacker}**: Bambazoo...Bamba... Bambamala.. fool em! **{attacker}** sends a clone and fools his enemies."
        "immune fpr ***{value}*** rounds!",
        lambda: function_collection.change_player_immune(current_ctx_global, attacker_global, 3),
        3,
        0,
        settings.dict_special + "bamboozled.jpg"
    ],
    [
        "**{attacker}** hides in a corner and waits for **{defender}**. Years passed. "
        "***{value} damage*** to **{attacker}**!",
        lambda: function_collection.change_player_hp(current_ctx_global, attacker_global, -20),
        20,
        0,
        settings.dict_special + "camper.jpg"
    ],
    [
        "**{attacker}** feels like an adult, but is only 17 years old. Stun for ***{value} rounds***!",
        lambda: function_collection.change_player_stun(current_ctx_global, attacker_global, 4),
        4,
        0,
        settings.dict_special + "teen.jpg"
    ],
    [
        "**{attacker}** walks slowly. IT'S HIGH NOON............DRAW! ***{value} damage*** to **EVERYONE except {attacker}**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -15, -1, exception=attacker_global),
        15,
        -1,
        settings.dict_special + "highnoon.gif"
    ],
    [
        "**{attacker}** has enough and takes out a letter. AN ACCUSATION FOR COPYRIGHT! **{defender}** "
        "never heard about article 13 and gets {value} years into prison! ***stun*** "
        "for ***{value} rounds***!",
        lambda: function_collection.change_player_stun(current_ctx_global, defender_global, 4),
        4,
        1,
        settings.dict_special + "article13.jpg"
    ]
]