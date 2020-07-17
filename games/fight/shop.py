# Attacker can roll a special while he attacks
# Will not happen if any player is offline
# 3 items will randomly get chosen from an item pool and the user can then decide which one to choose

import asyncio
import random
import settings
import games.fight.function_collection as function_collection

# Global variables are important so we can use lambda functions
current_player = None
current_ctx = None

async def enter(ctx, player):
    global current_player
    global current_ctx
    current_player = player
    current_ctx = ctx

    # We choose 3 items to show
    # It's not possible that one item is multiple times in the list
    all_items = shopItems[:]
    item_collection = []
    while len(item_collection) < 3:
        random_item = random.choice(all_items)
        all_items.remove(random_item)
        item_collection.append(random_item)

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

    # We wait 8 seconds (Sometimes it's less depending on the speed of the bot) for the user (Who entered the store) to choose an item
    try:
        choose = await settings.bot.wait_for('message', timeout=8, check=lambda choose: choose.author.name == player.name)
    except asyncio.TimeoutError:
        # Player was too slow to choose an item. So we leave the shop and the player doesn't get anything
        await ctx.send("Time is over!")
        return

    # Player wrote something. We check what the chose
    else:
        if choose.content == "1":
            await item_collection[0][3]()
        elif choose.content == "2":
            await item_collection[1][3]()
        elif choose.content == "3":
            await item_collection[2][3]()
        # If the player did write something but not a number from 1 to 3 this message gets posted
        else:
            await ctx.send(
                "**" + player.name + "**" + " don't know how numbers work.")


# Collection of items that can be in the store
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
        lambda: function_collection.change_player_hp(current_ctx, current_player, 20),
        "🍌"
    ],
    [
        'Sushi',
        '{symbol}**{name}** (+{value} dodging)',
        5,
        lambda: function_collection.change_player_dodge(current_ctx, current_player, 5),
        "🍣"
    ],
    [
        'Spoon',
        '{symbol}**{name}** (+{value} normal damage)',
        5,
        lambda: function_collection.change_player_attack(current_ctx, current_player, 5),
        "🥄"
    ],
    [
        "Laugh Emoji",
        '{symbol}**{name}** ({value} HP)',
        -100,
        lambda: function_collection.change_player_hp(current_ctx, current_player, -100),
        "🤣"
    ],
    [
        "Shield",
        '{symbol}**{name}** (+{value} immunity)',
        2,
        lambda: function_collection.change_player_immune(current_ctx, current_player, 2),
        "🛡"
    ],
    [
        "Michael Jackson",
        '{symbol}**{name}** (+{value} normal damage)',
        6,
        lambda: function_collection.change_player_attack(current_ctx, current_player, 6),
        "🕴"
    ],
    [
        "Dog",
        '{symbol}**{name}** (+{value} immunity)',
        3,
        lambda: function_collection.change_player_immune(current_ctx, current_player, 3),
        "🐶"
    ],
    [
        "Mathbook",
        '{symbol}**{name}** (+{value} HP)',
        50,
        lambda: function_collection.math_book(current_ctx, current_player, 50),
        "📘"
    ]
]