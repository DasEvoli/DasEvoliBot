# Attacker can enter the shop by a defined chance in settings.py
# Will not happen if any player is offline
# 3 items will randomly get chosen from an item pool and the user then decides which one he/she wants.

import asyncio
import random
import games.fight.function_collection as function_collection, settings

async def enter(ctx, player):
    # [0] = Name of item
    # [1] = How item gets posted
    # [2] = Value of that item
    # [3] = Lambda Function
    # [4] = Emoji to show before the item (Better overview)
    shopItems = [
        [
            'Banana',
            '{symbol}**{name}** (+{value} HP)',
            20,
            function_collection.change_player_hp(ctx, player, 20),
            "🍌"
        ],
        [
            'Sushi',
            '{symbol}**{name}** (+{value} dodging)',
            5,
            function_collection.change_player_dodge(ctx, player, 5),
            "🍣"
        ],
        [
            'Spoon',
            '{symbol}**{name}** (+{value} normal damage)',
            5,
            function_collection.change_player_attack(ctx, player, 5),
            "🥄"
        ],
        [
            "Laugh Emoji",
            '{symbol}**{name}** ({value} HP)',
            -100,
            function_collection.change_player_hp(ctx, player, -100),
            "🤣"
        ],
        [
            "Shield",
            '{symbol}**{name}** (+{value} immunity)',
            2,
            function_collection.change_player_immune(ctx, player, 2),
            "🛡"
        ],
        [
            "Michael Jackson",
            '{symbol}**{name}** (+{value} normal damage)',
            6,
            function_collection.change_player_attack(ctx, player, 6),
            "🕴"
        ],
        [
            "Dog",
            '{symbol}**{name}** (+{value} immunity)',
            3,
            function_collection.change_player_immune(ctx, player, 3),
            "🐶"
        ],
        [
            "Mathbook",
            '{symbol}**{name}** (+{value} HP)',
            50,
            function_collection.math_book(ctx, player, 50),
            "📘"
        ]
    ]

    # We show 3 items that the player can choose
    # It's not possible that one item is multiple times in the list
    item_collection = shopItems[:]
    while len(item_collection) > 3:
        item_collection.remove(random.choice(item_collection))

    # Message that gets posted in chat. Now the player has to choose his item
    await ctx.send("{0.mention} enters the Itemstore! Choose a number!\n".format(player.user) +
                        "1: " + item_collection[0][1].format(value=str(item_collection[0][2]),
                                                            name=item_collection[0][0],
                                                            symbol=item_collection[0][4]) + "\n" +
                        "2: " + item_collection[1][1].format(value=str(item_collection[1][2]),
                                                            name=item_collection[1][0],
                                                            symbol=item_collection[1][4]) + "\n" +
                        "3: " + item_collection[2][1].format(value=str(item_collection[2][2]),
                                                            name=item_collection[2][0],
                                                            symbol=item_collection[2][4]) + "\n")

    # We wait 8 seconds for the player to choose an item. Sometimes the time is shorter which is a problem by Async
    try:
        pick = await settings.bot.wait_for('message', timeout=8, check=lambda choose: choose.author.name == player.name)
    except asyncio.TimeoutError:
        # Player was too slow to choose an item. So we leave the shop and the player doesn't get anything
        await ctx.send("Time is over!")
        return

    # Player picked an item
    else:
        if pick.content == "1":
            await item_collection[0][3]()
        elif pick.content == "2":
            await item_collection[1][3]()
        elif pick.content == "3":
            await item_collection[2][3]()
        else:
            await ctx.send("**" + player.name + "**" + " doesn't know how numbers work.")