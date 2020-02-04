# Starting point and main interface of the bot

import discord
import games.fight.main
import settings
import utils
import datetime
import asyncio

# If this boolean is true then users can't use the bot and get an error message. You can change the name for whom it should work.
debug_mode = False
# Here you can specify who can use the bot while it's in debug mode
debug_name = "DasEvoli"

# Gets called when starting the bot
@utils.bot.event
async def on_ready():
    print('Bot is logged in as: ' + utils.bot.user.name)
    print(datetime.datetime.now())
    print("Online in:\n")
    # Prints every server the bot is on
    for guild in utils.bot.guilds:
        print(guild.name)


# Starts the fighting game between all players who are mentioned + author
# Example: "$fight @user1 @user2"
# Unlimited amount players possible but more than 10 is not suggested and atleast 2 are needed
# Important: You can also play with users who are offline

@utils.bot.command()
async def fight(ctx):
    if debug_mode:
        if ctx.message.author.name != debug_name:
            await ctx.send("Es wird gerade am Bot gearbeitet. Bitte versuche es später nocheinmal.")
            return
    
    # So you can see if anyone uses this command on their server
    print(datetime.datetime.now())
    print("Fight wird gestartet von " + ctx.message.author.name)

    # If this boolean is false, we deactivate all interactive events because it would be unfair otherwise
    all_online = True

    # All the mentions get added to the fight game + author (That means it is not possible to let other players fight. Important because we save fighting stats)
    fighterlist = ctx.message.mentions
    fighterlist.append(ctx.message.author)

    # We clear the playerlist because it's possible that someone got mention multiple times or author mentioned himself. No player should be able to be multiple times in a game
    # We also check if everyone is online
    cleared_list = []
    i = 0
    while i < len(fighterlist):
        if fighterlist[i] not in cleared_list:
            cleared_list.append(fighterlist[i])
            if fighterlist[i].status.name == 'offline':
                all_online = False
        i += 1

    # We need at least 2 players for the game to work
    if len(cleared_list) < 2:
        await ctx.send("Zum Kämpfen musst zu mindestens einen Gegner wählen!")
        return
    # If anyone is offline, interactions are getting deactivated
    if not all_online:
        await asyncio.sleep(2)
        await ctx.send("Nicht alle genannten Spieler sind online. Der Shop wird deshalb deaktiviert für dieses Match")

    # Game will be created now
    game_object = games.fight.main.Fight(ctx, cleared_list, all_online)
    await game_object.start()


# Simple command to clear chat in a channel. Was not possible to do in Discord when I created that function
# amount parameter is how many messages you want to delete (from last to first)
# -1 as argument will delete every message in that channel (Capped to 9999 so it's possible you need to call it multiple times)

@utils.bot.command()
async def clear(ctx, amount: int):
    if amount == -1:
        await ctx.channel.purge(limit=9999)
        return
    await ctx.channel.purge(limit=amount)


# Starts bot
# You need to add your token into the settings file
utils.bot.run(settings.Token)
