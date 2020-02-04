# Events can happen during a fight and affect multiple players
# It gets announced and an image will be posted

import discord
import asyncio
import random
import utils
import games.fight.function_collection as function_collection

# We need to use global variables because we use Lambda functions
alive_players_global = []
all_players_global = []
current_ctx_global = None

async def start_event(ctx, all_players, alive_players):
    global alive_players_global, all_players_global, current_ctx_global
    all_players_global = all_players
    alive_players_global = alive_players
    current_ctx_global = ctx

    # Events are something big with a low chance. So it gets announced with customizable strings. In those strings 2 random players are getting mentioned 
    # Can't be one player multiple times
    random_player_one = random.choice(alive_players_global)
    random_player_two = random.choice(alive_players_global)
    while random_player_two == random_player_one:
        random_player_two = random.choice(alive_players_global)
    random.choice(listEventAnnounce).format(player1=random_player_one.name,
                                            player2=random_player_two.name)
    await asyncio.sleep(4)
    event = random.choice(listEvents)
    await ctx.send(str(event[0]).format(value=event[2]))
    # We always send an image in chat if an event happens
    await ctx.send(file=discord.File(event[4]))
    await asyncio.sleep(2)
    # Lambda gets called in list
    await event[1]()


# [0] = Text that gets posted in chat
# [1] = Lambda Function
# [2] = Value
# [3] = count. How many players will be affected. -1 = all players
# [4] = Image that gets postet when this event is happening

listEvents = [
    [
        "Die Erde fängt spürbar zu erzittern an. Ist es ein Erdbeben? OH NEIN, DIE **GAMESCOM** WURDE ERÖFFNET. Schnell werdet "
        "ihr überrannt von zu vielen Menschen, die Gronkh umarmen wollen. \n***{value} Schaden*** an **ALLE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -30, -1),
        30,
        -1,
        utils.dict_event + "gamescom.jpg"
    ],
    [
        "Am Himmel zeichnet sich ein Schatten ab. ES IST HANZO! Ein ohrenbetäubendes Geräusch erschüttert die Umgebung. RYUU GA WAGA TEKI WO KURAU. "
        "***{value} Schaden*** an **ALLE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -30, -1),
        30,
        -1,
        utils.dict_event + "hanzo.gif"
    ],
    [
        "Nadja wirft mit Nudelsalat. Unendlich viele Spirellis fliegen durch die Luft! ***{value} Schaden*** an **ALLE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -15, -1),
        15,
        -1,
        utils.dict_event + "wurstsalat.jpg"
    ],
    [
        "Quax schreibt einen Virus und verteilt diesen über ein Furryporn Link. Alle klicken drauf! **ALLE** können ***{value}%*** weniger dodgen!",
        lambda: function_collection.change_players_dodge(current_ctx_global, alive_players_global, -15, -1),
        15,
        -1,
        utils.dict_event + "hacker.jpg"
    ],
    [
        "Ohhh eine wunderschöne Frau! OH NEIN, ES IST SNEAKY! ***{value} Schaden*** an **ALLE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -20, -1),
        20,
        -1,
        utils.dict_event + "sneaky.jpg"
    ],
    [
        "Nymeria wirft mit Käsekuchen! Oh nein, da sind Mandarinen drin! ***{value} Schaden*** an **ALLE**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -20, -1),
        20,
        -1,
        utils.dict_event + "käsekuchen.jpg"
    ],
    [
        "Nymeria wirft mit Käsekuchen! Keine Mandarinen. Gelobt sei Nomeria! ***{value} Heilung*** an **ALLE**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, 30, -1),
        30,
        -1,
        utils.dict_event + "käsekuchenheal.jpg"
    ],
    [
        "Fiyora holt tief Luft und schreit durch die Gegend! Eine regelrechte Explosion! ***Stun für {value} Runden*** an **ALLE**!",
        lambda: function_collection.change_players_stun(current_ctx_global, alive_players_global, 4, -1),
        4,
        -1,
        utils.dict_event + "fiyora.jpg"
    ],
    [
        "Lego hat mal wieder zwei Emotes entfernt und dafür ein Neues hinzugefügt. Einfach unglaublich. "
        "Stun für ***{value} Runden*** an **drei zufällige Spieler**!",
        lambda: function_collection.change_players_stun(current_ctx_global, alive_players_global, 4, 3),
        4,
        3,
        utils.dict_event + "gekucringe.jpg"
    ],
    [
        "Vodafone kriegt es nicht gebacken, ein neues Handy loszuschicken. Zwei Mitarbeiter von der Telekom können das nicht fassen. "
        "***{value} Schaden*** an **2 zufällige Spieler**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -20, 2),
        20,
        2,
        utils.dict_event + "vodafone.jpg"
    ],
    [
        "Am Himmel zeichnet sich eine Gestalt ab. Ein heiliger Schein blendet eure Augen. **Alle** verstorbenen Spieler werden mit ***{value} HP"
        " wiederbelebt***.",
        lambda: function_collection.revive_players(current_ctx_global, alive_players_global, all_players_global, 30, -1),
        30,
        -1,
        utils.dict_event + "obiwan.jpg"
    ]
]

# Events are something big with a low chance. So it gets announced with customizable strings. In those strings 2 random players are getting mentioned 
listEventAnnounce = [
    "**{player1}** und **{player2}** spüren eine Erschütterung der Macht...",
    "**{player1}** dreht sich schnell um und spürt, dass etwas nicht stimmt...",
    "Der Wind hat ungünstige Winde. **{player1}** bereitet sich auf eine Katastrophe vor...",
    "**{player1}** beendet sofort seinen Stream. Was wird passieren...",
    "**{player1}** lässt ein Löffel beim Cornflakes essen fallen. Was ist los?",
    "(jazz music stops)...",
    "(lute playing stops)...",
    "(banjo music stops)...",
    "**{player1}** kann es kaum aussprechen, als er etwas in der Ferne erkannte..."
]