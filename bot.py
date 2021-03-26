import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils import files

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().default()
intents.members = True

bot = commands.Bot(command_prefix = '!', intents = intents)

# Load bot commands
for file in files.get_py_files('commands'):
    bot.load_extension('commands.' + file)

bot.run(TOKEN)