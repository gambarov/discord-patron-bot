import discord
from discord.ext.commands import Bot

intents = discord.Intents().default()
intents.members = True

class Patron:
    def __init__(self, bot):
        self.bot = Bot(command_prefix='!', intents=intents)
        