# Events can happen during a fight and affect multiple players
# It gets announced and an image will be posted

import asyncio
import random
import settings
import games.fight.function_collection as function_collection
import discord

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
        "The earth starts to tremble. Is it an earthquake? OH MO, THE **GAMESCOM** ***{value} damage*** to **EVERYONE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -30, -1),
        30,
        -1,
        settings.dict_event + "gamescom.jpg"
    ],
    [
        "There is a shadow in the sky. IT'S HANZO! A loud scream is to hear. RYUU GA WAGA TEKI WO KURAU."
        "***{value} damage*** to **EVERYONE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -30, -1),
        30,
        -1,
        settings.dict_event + "hanzo.gif"
    ],
    [
        "Oh a beautiful Frau! OH NO, IT'S SNEAKY! ***{value} damage*** to **EVERYONE**!",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -20, -1),
        20,
        -1,
        settings.dict_event + "sneaky.jpg"
    ],
    [
        "Someone throws Cheese Cake! OH NO, it has Oranges in it! ***{value} damage*** to **EVERYONE**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, -20, -1),
        20,
        -1,
        settings.dict_event + "cheesecake.jpg"
    ],
    [
        "Someone throws Cheese Cake! No Oranges. That tastes good! ***{value} healing*** for **EVERYONE**",
        lambda: function_collection.change_players_hp(current_ctx_global, alive_players_global, 30, -1),
        30,
        -1,
        settings.dict_event + "cheesecakeheal.jpg"
    ],
    [
        "Someone screams! It's like an explosion! ***Stun for {value} rounds*** to **EVERYONE**!",
        lambda: function_collection.change_players_stun(current_ctx_global, alive_players_global, 4, -1),
        4,
        -1,
        settings.dict_event + "nkorea.jpg"
    ],
    [
        "A person is emerging from the sky. A holy appearance is blending you. **Everyone** gets revived with ***{value} HP***.",
        lambda: function_collection.revive_players(current_ctx_global, alive_players_global, all_players_global, 30, -1),
        30,
        -1,
        settings.dict_event + "obiwan.jpg"
    ]
]

# Events are something big with a low chance. So it gets announced with customizable strings. In those strings 2 random players are getting mentioned 
listEventAnnounce = [
    "**{player1}** and **{player2}** feel a disturbance in the force...",
    "**{player1}** turns around and feels that something is wrong...",
    "Unfavorable winds **{player1}** is preparing itself for something...",
    "**{player1}** ends her/his stream immediately. What is happening...",
    "**{player1}** drops his spoon while eating cereals. What's wrong?",
    "(jazz music stops)...",
    "(lute playing stops)...",
    "(banjo music stops)..."
]