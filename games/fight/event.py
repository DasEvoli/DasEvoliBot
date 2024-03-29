# Events can happen during a fight and affects multiple players
# Events are something big and should have a low chance in settings.py

import asyncio
import random
import discord
import os
from games.fight import function_collection, settings

async def start_event(ctx, all_players, alive_players):
    # [0] = String that gets sent when this event is happening
    # [1] = Lambda Function
    # [2] = Value
    # [3] = count. How many players will be affected. -1 = all players
    # [4] = Image that gets postet when this event is happening
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    listEvents = [
        [
            "The earth starts to tremble. Is it an earthquake? OH NO, THE **GAMESCOM** JUST OPENED ***{value} damage*** to **EVERYONE**!",
            lambda: function_collection.change_players_hp(ctx, alive_players, -30, -1),
            30,
            -1,
            curr_dir + settings.dir_event + "gamescom.jpg"
        ],
        [
            "There is a shadow in the sky. IT'S HANZO! A loud scream is to hear. RYUU GA WAGA TEKI WO KURAU."
            "***{value} damage*** to **EVERYONE**!",
            lambda: function_collection.change_players_hp(ctx, alive_players, -30, -1),
            30,
            -1,
            curr_dir + settings.dir_event + "hanzo.gif"
        ],
        [
            "Oh a beautiful woman! OH NO, IT'S SNEAKY! ***{value} damage*** to **EVERYONE**!",
            lambda: function_collection.change_players_hp(ctx, alive_players, -20, -1),
            20,
            -1,
            curr_dir + settings.dir_event + "sneaky.jpg"
        ],
        [
            "Someone baked Cheese Cake! OH NO, it has Oranges in it! ***{value} damage*** to **EVERYONE**",
            lambda: function_collection.change_players_hp(ctx, alive_players, -20, -1),
            20,
            -1,
            curr_dir + settings.dir_event + "cheesecake.jpg"
        ],
        [
            "Someone baked Cheese Cake! No Oranges. That tastes good! ***{value} healing*** for **EVERYONE**",
            lambda: function_collection.change_players_hp(ctx, alive_players, 30, -1),
            30,
            -1,
            curr_dir + settings.dir_event + "cheesecakeheal.jpg"
        ],
        [
            "Someone screams! It's like an explosion! ***Stun for {value} rounds*** to **EVERYONE**!",
            lambda: function_collection.change_players_stun(ctx, alive_players, 4, -1),
            4,
            -1,
            curr_dir + settings.dir_event + "nkorea.jpg"
        ],
        [
            "A person is emerging from the sky. A holy appearance is blending you. **Everyone** gets revived with ***{value} HP***.",
            lambda: function_collection.revive_players(ctx, alive_players, all_players, 30, -1),
            30,
            -1,
            curr_dir + settings.dir_event + "obiwan.jpg"
        ]
    ]
    # We announce the event with a string that gets 2 random alive players as input
    random_player_one = random.choice(alive_players)
    random_player_two = random.choice(alive_players)
    while random_player_two == random_player_one:
        random_player_two = random.choice(alive_players)
    await ctx.send(random.choice(listEventAnnounce).format(player1=random_player_one.name, player2=random_player_two.name))

    await asyncio.sleep(settings.event_delay)

    event = random.choice(listEvents)
    await ctx.send(str(event[0]).format(value=event[2]))
    await ctx.send(file=discord.File(event[4]))
    await asyncio.sleep(settings.default_delay)
    await event[1]()

listEventAnnounce = [
    "**{player1}** and **{player2}** are feeling a disturbance in the force...",
    "**{player1}** turns around and feels that something is wrong...",
    "Unfavorable winds **{player1}** is preparing itself for something...",
    "**{player1}** ends her/his stream immediately. What is happening...",
    "**{player1}** drops his spoon while eating cereals. What's wrong?",
    "(jazz music stops)...",
    "(lute playing stops)...",
    "(banjo music stops)..."
]