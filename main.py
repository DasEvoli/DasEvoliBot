# Starting point and main interface of the bot

import games.fight.main
import games.love.main
import alert.twitch
import settings
import datetime
import time
import asyncio
import os
import discord

# Gets called when starting the bot
@settings.bot.event
async def on_ready():
    print('Bot is logged in as: ' + settings.bot.user.name)
    print(datetime.datetime.now())
    print("Servers that use this bot:")
    # Prints every server the bot is on
    for guild in settings.bot.guilds:
        print(guild.name)

    # Object for alert module
    # Todo Outsourcing would be better so the bot works without this module
    alert_obj = alert.twitch.main()
    # Starting checking for alerts. This function loops in a separate thread
    await alert_obj.check_alerts()

@settings.bot.command()
async def commands(ctx):
    await ctx.send("$fight name1 name2 name3... (Starts a fighting game. Unlimited players. You don't need to add yourself)")
    await ctx.send("$clear -1 (Clears as many messages as possible)")
    await ctx.send("$clear 1 (Clears the last message. This number is adjustable)")
    await ctx.send("$twitch_alert twitchname (Removes or adds a new Twitch alert)")
    await ctx.send("$love name1 (shows how strong your love is with name1)")


# Starts the fighting game between all players who are mentioned + author
# Example: "$fight @user1 @user2"
# Unlimited amount players possible but more than 10 is not suggested and at least 2 are needed
# Important: You can also play with users who are offline

@settings.bot.command()
async def fight(ctx):
    # So you can see if anyone uses this command on their server
    print(datetime.datetime.now())
    print("Fight started by " + ctx.message.author.name)

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
        await ctx.send("You need to choose at least one opponent lapp ")
        return
    # If anyone is offline, interactions are getting deactivated
    if not all_online:
        await asyncio.sleep(2)
        await ctx.send("Not all players are online. Shop will be deactivated in this game.")

    # Game will be created now
    game_object = games.fight.main.Fight(ctx, cleared_list, all_online)
    await game_object.start()


# Simple command to clear chat in a channel. Was not possible to do in Discord when I created that function
# amount parameter is how many messages you want to delete (from last to first)
# -1 as argument will delete every message in that channel (Capped to 9999 so it's possible you need to call it multiple times)

@settings.bot.command()
async def clear(ctx, amount: int):
    if amount == -1:
        await ctx.channel.purge(limit=9999)
        return
    await ctx.channel.purge(limit=amount)


# Command to add the username of a twitch channel to an alert list. Next time the user goes online your channel where you used this command will get a notification
# with a cooldown (currently 12 hours)

@settings.bot.command()
async def twitch_alert(ctx, twitch_channel=""):
    if twitch_channel == "":
        await ctx.send("No Twitch channel defined.")
        return
    twitch_channel = twitch_channel.lower()
    # If discord server is not in the alert list, we add it
    if not alert.twitch.json_handler.discord_server_exists(ctx.guild.name):
        alert.twitch.json_handler.add_discord_server(ctx.guild.name)
    # If alert already exist we remove it. If alert doesn't exist, we add it
    if not alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
        alert.twitch.json_handler.add_twitch_channel(ctx.guild.name, twitch_channel, ctx.channel.id)
        if alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
            await ctx.send("**{}** was added successfully to the Twitch alert list. As soon as this Twitch channel goes online this discord channel gets a notification.".format(twitch_channel))
    else:
        alert.twitch.json_handler.remove_twitch_channel(ctx.guild.name, twitch_channel)
        if not alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
            await ctx.send("**{}** was removed successfully from the alert list. This discord channel will not get any notifications anymore if this Twitch channel goes online.".format(twitch_channel))    

# Little game that prints a random number between 0 - 100 to show love between 2 users    
@settings.bot.command()
async def love(ctx):
    author = ctx.message.author
    mentionlist = ctx.message.mentions
    if len(mentionlist) > 1:
        await ctx.send("Stop! You can't calculate your love for more than 1 person on this discord server!")
        return 
    elif len(mentionlist) == 0:
        await ctx.send("To calculate your love to someone you need to specify one person.")
        return
    else: 
        name = mentionlist[0]
        await games.love.main.calculate_love(ctx, author, name)
    



# Starts bot
# You need to add your token into the settings file
settings.bot.run(settings.token)
