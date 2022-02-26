from discord.ext import commands

# If this boolean is true then users can't use the bot and get an error message. You can change the name for whom it should work.
debug_mode = False
# If you enable debug mode this username still can use the bot. This needs to be your Discord name without your id. DasEvoli instead of DasEvoli#123
debug_name = ""

# Your Discord Bot Token.
token = ""

# Twitch api settings. Token will automatically be generated.
client_id = ""
client_secret = ""
access_token = ""

# Delay before alerts are getting checked again.
twitch_alert_check_delay = 10
# Cooldown before an alert gets triggered again for a certain channel in seconds.
twitch_alert_cooldown = 3600

# Dictionaries to store images that can be posted by the bot for events in the fighting game
dict_event = ""
dict_special = ""
dict_random = ""

# Command prefix so the bot listen to your commands. Can interfere with other bots
bot = commands.Bot(command_prefix='$')