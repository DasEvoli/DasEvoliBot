import games.fight.main
import games.love.main
import alert.twitch
import settings
import datetime


@settings.bot.event
async def on_ready():
    print('Bot is logged in as: ' + settings.bot.user.name)
    print(datetime.datetime.now())
    print("Servers that use this bot:")
    for guild in settings.bot.guilds:
        print(guild.name)

    # Start checking for alerts. This function loops in a separate thread
    alert_twitch_obj = alert.twitch.main()
    await alert_twitch_obj.check_alerts()

# Prints the command list
@settings.bot.command()
async def commands(ctx):
    command_string = "`"
    command_string += "$fight <name1> <name2> <name3>... - Starts a fighting game. You don't need to add yourself\n"
    command_string += "$clear <amount> - Clears messages (newest -> oldest) -1 clears as many messages as possible\n"
    command_string += "$twitch_alert <twitchname> - Removes or adds a new Twitch alert\n"
    command_string += "$love <name1> - shows how strong your love is with name1\n"
    command_string += "`"
    await ctx.send(command_string)

# Starts the fighting game between all players who are mentioned + author
# Example: "$fight @user1 @user2"
# Unlimited amount players possible but more than 10 is not suggested and at least 2 are needed
# Important: You can also play with users who are offline but then certain actions will be disabled
# The result gets stored in a file that can be printed with a command
@settings.bot.command()
async def fight(ctx):
    print(datetime.datetime.now())
    print("Fight started by " + ctx.message.author.name)
    all_online = True
    fighterlist = ctx.message.mentions
    fighterlist.append(ctx.message.author)
    # We sanitize the playerlist because it's possible that someone got mention multiple times or author mentioned himself
    cleared_list = []
    i = 0
    while i < len(fighterlist):
        if fighterlist[i] not in cleared_list:
            cleared_list.append(fighterlist[i])
            if fighterlist[i].status.name == 'offline':
                all_online = False
        i += 1
    for fighter in fighterlist:
        if fighter not in cleared_list:
            cleared_list.append(fighter)
            if fighter.status.name == 'offline': all_online = False
    if len(cleared_list) < 2:
        await ctx.send("You need to choose at least one opponent.")
        return
    if not all_online:
        await ctx.send("Not all players are online. Shop will be deactivated in this game.")
    game_object = games.fight.main.Fight(ctx, cleared_list, all_online)
    await game_object.start()

# Simple command to clear chat in a channel.
# amount parameter how many messages you want to delete (beginning from last)
# Amount will be increased by one because sending the command counts as message
# -1 as argument will delete every message in that channel limited to 9999
@settings.bot.command()
async def clear(ctx, amount: int):
    if amount == -1:
        await ctx.channel.purge(limit=9999)
    await ctx.channel.purge(limit=amount-1)


# Command to add the username of a twitch channel to an alert list
# Next time the user goes online the channel where you used this command will get a notification
@settings.bot.command()
async def twitch_alert(ctx, twitch_name: str):
    if not twitch_name:
        await ctx.send("No Twitch channel defined.")
        return
    twitch_name = twitch_name.lower()
    # If discord server is not in the alert list, we add it
    if not alert.twitch.json_handler.twitch_name_exists(twitch_name):
        alert.twitch.json_handler.add_twitch_name(twitch_name)
    # If alert already exist we remove it. If alert doesn't exist, we add it
    if not alert.twitch.json_handler.discord_channel_id_exists(ctx.channel.id, twitch_name):
        alert.twitch.json_handler.add_discord_channel_id(ctx.channel.id, twitch_name)
        if alert.twitch.json_handler.discord_channel_id_exists(ctx.channel.id, twitch_name):
            await ctx.send("**{}** was added successfully to the Twitch alert list. As soon as this Twitch channel goes online this discord channel gets a notification.".format(twitch_name))
    else:
        alert.twitch.json_handler.remove_discord_channel_id(ctx.channel.id, twitch_name)
        if not alert.twitch.json_handler.discord_channel_id_exists(ctx.channel.id, twitch_name):
            await ctx.send("**{}** was removed successfully from the alert list. This discord channel will not get any notifications anymore if this Twitch channel goes online.".format(twitch_name))    

# Little game that prints a random number between 0 - 100 to show love between 2 users    
@settings.bot.command()
async def love(ctx):
    author = ctx.message.author
    mentionlist = ctx.message.mentions
    if len(mentionlist) > 1:
        await ctx.send("Stop! You can't calculate your love for more than 1 person!")
        return 
    elif len(mentionlist) == 0:
        await ctx.send("To calculate your love to someone you need to specify one person.")
        return
    else: 
        await games.love.main.calculate_love(ctx, author, mentionlist[0])
    
# Starts bot
settings.bot.run(settings.token)
