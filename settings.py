import os

# If this boolean is true then users can't use the bot and get an error message. You can change the name for whom it should work.
debug_mode = False
# If you enable debug mode this name still can use the bot
debug_name = "DasEvoli"

# Bot Token
token = "NTQ5ODMxODk2NzU5MTQwMzUz.XjlJLg.lepVHrBYdL5H8zWGRfFX1TX8bIM"
# Twitch information. Do not make it public!
client_id = "4ew27s87vvvhp4a6zaugpx2c3yccuk"
client_secret = "jhkzjp3adg1h25nbixqgeqers7d7n6"
api_token = ""

# Dictionaries to store images that can be posted by the bot for special events like the fighting game
dict_event = os.path.dirname(os.path.realpath(__file__)) + "\\games\\fight\\resources\\event\\"
dict_special = os.path.dirname(os.path.realpath(__file__)) + "\\games\\fight\\resources\\special\\"
dict_random = os.path.dirname(os.path.realpath(__file__)) + "\\games\\fight\\resources\\random\\"

# Command prefix so the bot listen to your commands. Can interfere with other bots
# Also we are using this name now in the whole project to access the bot directly
from discord.ext import commands
bot = commands.Bot(command_prefix='$')