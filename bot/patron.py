import discord
from discord.ext.commands import Bot

from utils import files

from bot.config import options

class Patron:
    def __init__(self):
        self.bot = Bot(**options)
        self._load_extensions('commands')
        self._load_extensions('events')
        self.bot.load_extension('commands.exchange.command')

    def run(self, token):
        self.bot.run(token)

    def _load_extensions(self, system):
        for file in files.get_py_files(system):
            self.bot.load_extension('{}.{}'.format(system, file))
        