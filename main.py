import os

from discord.ext import commands
from dotenv import load_dotenv

from bot.patron import Patron

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Patron()
bot.run(TOKEN)