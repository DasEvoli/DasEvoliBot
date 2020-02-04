# This file contains basic utility like the object reference to the bot or paths of dictionaries

from discord.ext import commands

# Dictionaries to store images that can be posted by the bot for special events like the fighting game
dict_event = "resources/event/"
dict_special = "resources/special/"
dict_random = "resources/random/"

# Command prefix so the bot listen to your commands. Can interfere with other bots
# Also we are using this name now in the whole project to access the bot directly
bot = commands.Bot(command_prefix='$')