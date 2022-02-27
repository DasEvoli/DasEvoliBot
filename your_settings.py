from discord.ext import commands

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