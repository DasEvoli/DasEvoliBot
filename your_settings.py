import os

# Settings File you need to adjust to use your bot

# If this boolean is true then users can't use the bot and get an error message. You can change the name for whom it should work.
debug_mode = False
# If you enable debug mode this name still can use the bot. This needs to be your Discord name without your id. DasEvoli instead of DasEvoli#123
debug_name = ""

# Bot Token
token = ""
# Twitch api settings
client_id = ""
client_secret = ""
api_token = ""

# Dictionaries to store images that can be posted by the bot for special events like the fighting game
dict_event = ""
dict_special = ""
dict_random = ""

# Command prefix so the bot listen to your commands. Can interfere with other bots
# We are also using this name now in the whole project to access the bot directly
from discord.ext import commands
bot = commands.Bot(command_prefix='$')