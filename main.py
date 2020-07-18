# Starting point and main interface of the bot

import games.fight.main
import alert.twitch
import settings
import datetime
import time
import asyncio
import os

# Gets called when starting the bot
@settings.bot.event
async def on_ready():
    print('Bot is logged in as: ' + settings.bot.user.name)
    print(datetime.datetime.now())
    print("Servers that use this bot:")
    # Prints every server the bot is on
    for guild in settings.bot.guilds:
        print(guild.name)

    # Setup files
    #if not os.path.isfile("alert/channels.json"):

    #if not os.path.isfile("games/fight/fight_statistics.json"):
        #file = open('games/fight/fight_statistics.json', 'w+')
        #file.close

    # Object for alert module
    # Outsourcing would be better so the bot works without this module
    alert_obj = alert.twitch.main()
    # Starting checking for alerts. This function loops in a separate thread
    await alert_obj.check_alerts()



# Starts the fighting game between all players who are mentioned + author
# Example: "$fight @user1 @user2"
# Unlimited amount players possible but more than 10 is not suggested and at least 2 are needed
# Important: You can also play with users who are offline

@settings.bot.command()
async def fight(ctx):
    if settings.debug_mode:
        if ctx.message.author.name != settings.debug_name:
            await ctx.send("I'm currently working on this bot. Please try again later.")
            return
    
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
    if settings.debug_mode:
        if ctx.message.author.name != settings.debug_name:
            await ctx.send("I'm currently working on this bot. Please try again later.")
            return
    if amount == -1:
        await ctx.channel.purge(limit=9999)
        return
    await ctx.channel.purge(limit=amount)


# Command to add the username of a twitch channel to an alert list. Next time the user goes online your channel where you used this command will get a notification
# with a cooldown (currently 12 hours)

@settings.bot.command()
async def add_twitch_alert(ctx, twitch_channel=""):
    if settings.debug_mode:
        if ctx.message.author.name != settings.debug_name:
            await ctx.send("I'm currently working on this bot. Please try again later.")
            return
    if twitch_channel == "":
        await ctx.send("No Twitch channel defined.")
        return
    twitch_channel = twitch_channel.lower()
    if not alert.twitch.json_handler.discord_server_exists(ctx.guild.name):
        alert.twitch.json_handler.add_discord_server(ctx.guild.name)
    if not alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
        alert.twitch.json_handler.add_twitch_channel(ctx.guild.name, twitch_channel, ctx.channel.id)
    if alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
        await ctx.send("**{}** was added successfully to the Twitch alert list. As soon as this Twitch channel goes online this discord channel gets a notification.".format(twitch_channel))
    else: await ctx.send("Error happend. Could not add **{}** to the alert list.".format(twitch_channel))     
            
     
# Command to remove the username of a twitch channel from the alert list. This also clears the cooldown.

@settings.bot.command()
async def remove_twitch_alert(ctx, twitch_channel=""):
    if settings.debug_mode:
        if ctx.message.author.name != settings.debug_name:
            await ctx.send("I'm currently working on this bot. Please try again later.")
            return
    if twitch_channel == "":
        await ctx.send("No Twitch channel defined.")
        return
    twitch_channel = twitch_channel.lower()
    if not alert.twitch.json_handler.discord_server_exists(ctx.guild.name):
        alert.twitch.json_handler.add_discord_server(ctx.guild.name)
    if not alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
        await ctx.send("**{}** does not exist in the alert list for this server.".format(twitch_channel))
        return
    else: alert.twitch.json_handler.remove_twitch_channel(ctx.guild.name, twitch_channel)
    if not alert.twitch.json_handler.twitch_channel_exists(ctx.guild.name, twitch_channel):
        await ctx.send("**{}** was removed successfully from the alert list. This discord channel will not get any notifications anymore if this Twitch channel goes online.".format(twitch_channel))
    else: await ctx.send("Error happend. Could not remove **{}** from the alert list.".format(twitch_channel))

# Starts bot
# You need to add your token into the settings file
settings.bot.run(settings.token)
