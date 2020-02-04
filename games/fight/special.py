# Attacker can roll a special while he attacks
# Image will be posted
# It can also be a negative special

import asyncio
import random
import utils
import discord
import games.fight.function_collection as function_collection

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
        "**{attacker}** nutzt Knuddelpower und drückt **{defender}** fast schon die letzte Luft aus der Lunge! Das sind ***{value} Schaden*** an **{defender}**!",
        lambda: function_collection.change_player_hp(current_ctx_global, defender_global, -30),
        30,
        1,
        utils.dict_special + "fluffy.gif"
    ],
    [
        "Wo ist **{attacker}**?  Oh nein! Der stündliche Waifu-Hunt hat begonnen. Kurzerhand verlässt **{attacker}** den Fight. Stun für ***{value} Runden*** "
        "an **{attacker}**, um neue Waifus zu claimen!",
        lambda: function_collection.change_player_stun(current_ctx_global, attacker_global, 4),
        4,
        0,
        utils.dict_special + "waifuhunt.jpg"
    ],
    [
        "**{attacker}** hat Lego vertraut und für heute ein gemeinsames Spiel ausgemacht. Lego ließ ihn überraschenderweise wieder mal Links liegen. ***Stun für "
        "{value} Runden*** an **{attacker}**!",
        lambda: function_collection.change_player_stun(current_ctx_global, attacker_global, 4),
        4,
        0,
        utils.dict_special + "lego_derp.jpg"
    ],
    [
        "**{attacker}** muss sich erholen und platziert etwas auf den Boden. Eine große Kuppel breitet sich um ihn aus. ***{attacker}*** ist "
        "***Immun*** für ***{value} Runden!***",
        lambda: function_collection.change_player_immune(current_ctx_global, attacker_global, 4),
        4,
        0,
        utils.dict_special + "gibraltar.jpg"
    ],
    [
        "**{attacker}** sieht, dass alle Spieler zusammenstehen. Panisch sucht er die Y auf der Tastatur. Ein Artillerieangriff! ***{value} Schaden***"
        " an **ALLE außer {attacker}**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -15, -1, exception=attacker_global),
        15,
        -1,
        utils.dict_special + "artillerie.jpg"
    ],
    [
        "**{attacker}** ballt die Faust und schlägt einen Tunnel. Versteckt im Void kann niemand ihn treffen. ***Immun für {value} Runden!***",
        lambda: function_collection.change_player_immune(current_ctx_global, attacker_global, 3),
        3,
        0,
        utils.dict_special + "void.jpg"
    ],
    [
        "**{attacker}**: Bambazoo...Bamba... Bambamala.. fool em! **{attacker}** schickt einen Klon vor und lenkt seinen Gegner ab."
        "Immun für ***{value}*** Runden!",
        lambda: function_collection.change_player_immune(current_ctx_global, attacker_global, 3),
        3,
        0,
        utils.dict_special + "bamboozled.jpg"
    ],
    [
        "**{attacker}** verschanzt sich in eine Ecke und wartet auf **{defender}**. Es vergingen Jahre, bis er aufgibt. Das hinterlässt Spuren. "
        "***{value} Schaden*** an **{attacker}**!",
        lambda: function_collection.change_player_hp(current_ctx_global, attacker_global, -20),
        20,
        0,
        utils.dict_special + "camper.jpg"
    ],
    [
        "**{attacker}** fühlt sich schon erwachsen, ist aber erst 17. Das ist nicht fair. Stun für ***{value} Runden***!",
        lambda: function_collection.change_player_stun(current_ctx_global, attacker_global, 4),
        4,
        0,
        utils.dict_special + "teen.jpg"
    ],
    [
        "**{attacker}** holt sich Ace zur Hilfe. Ace berührt **{defender}** und lässt ihn abstürzen! ***{value} Schaden*** an **{defender}**",
        lambda: function_collection.change_player_hp(current_ctx_global, defender_global, -20),
        20,
        1,
        utils.dict_special + "absturz.jpg"
    ],
    [
        "**{attacker}** verlangsamt sich bedrohend. IT'S HIGH NOON............DRAW! ***{value} Schaden*** an **ALLE außer {attacker}**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -15, -1, exception=attacker_global),
        15,
        -1,
        utils.dict_special + "highnoon.gif"
    ],
    [
        "**{attacker}** hat genug und zückt einen Brief aus der Tasche. EINE ANKLAGE FÜR EINE URHEBERRECHTSVERLETZUNG! **{defender}** "
        "hat noch nie etwas von Artikel 13 gehört und muss die Katzenbilder offline nehmen und {value} Jahre ins Gefängnis! ***Stun*** "
        "für ***{value} Runden***!",
        lambda: function_collection.change_player_stun(current_ctx_global, defender_global, 4),
        4,
        1,
        utils.dict_special + "artikel13.jpg"
    ]
]