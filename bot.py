import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().default()
intents.members = True

bot = commands.Bot(command_prefix = '!', intents = intents)

bot.load_extension('commands.who')
bot.load_extension('commands.choice')
bot.load_extension('commands.course')
bot.load_extension('commands.dict')

bot.run(TOKEN)